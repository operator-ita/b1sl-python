"""
sap_metadata_generator.parser
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Parses SAP B1 OData metadata.xml into intermediate structures.
"""
from __future__ import annotations

import json
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class SAPProperty:
    name: str
    edm_type: str
    nullable: bool = True
    max_length: int | None = None
    enum_type: str | None = None


@dataclass
class SAPComplexType:
    name: str
    properties: list[SAPProperty] = field(default_factory=list)


@dataclass
class SAPNavigationProperty:
    name: str
    target_type: str
    multiplicity: str  # "0..1" | "1" | "*"


@dataclass
class SAPEntityType:
    name: str
    service_name: str
    properties: list[SAPProperty] = field(default_factory=list)
    nav_properties: list[SAPNavigationProperty] = field(default_factory=list)
    key_properties: list[str] = field(default_factory=list)


@dataclass
class SAPEnumMember:
    name: str
    value: int


@dataclass
class SAPEnumType:
    name: str
    members: list[SAPEnumMember] = field(default_factory=list)


@dataclass
class ActionDef:
    name: str
    bound_entity_set: str | None = None
    is_bound: bool = False
    bound_type: str | None = None

@dataclass
class FunctionDef:
    name: str
    bound_entity_set: str | None = None
    is_bound: bool = False
    bound_type: str | None = None
    return_type: str = "Any"

@dataclass
class SAPEntitySet:
    name: str
    entity_type: str
    actions: list[ActionDef] = field(default_factory=list)
    functions: list[FunctionDef] = field(default_factory=list)
    description: str = "" # Enriched from HTML reference


@dataclass
class ParsedMetadata:
    entities: dict[str, SAPEntityType] = field(default_factory=dict)
    complex_types: dict[str, SAPComplexType] = field(default_factory=dict)
    enums: dict[str, SAPEnumType] = field(default_factory=dict)
    entity_sets: dict[str, SAPEntitySet] = field(default_factory=dict)
    raw_actions: list[ActionDef] = field(default_factory=list)
    raw_functions: list[FunctionDef] = field(default_factory=list)
    dedicated_services: dict[str, SAPEntitySet] = field(default_factory=dict)

    # Enrichment and Filtering
    service_document: list[str] = field(default_factory=list) # From service_document.json
    reference_cache: dict[str, Any] = field(default_factory=dict) # From reference_cache.json


NS = {
    "edmx": "http://docs.oasis-open.org/odata/ns/edmx",
    "edm":  "http://docs.oasis-open.org/odata/ns/edm",
}

NS_LEGACY = {
    "edmx": "http://schemas.microsoft.com/ado/2007/06/edmx",
    "edm":  "http://schemas.microsoft.com/ado/2008/09/edm",
}


def _should_skip(name: str) -> bool:
    """Ignore user defined objects, fields and specific prefixes for a Vanilla SDK."""
    # Common prefixes to skip in a general-purpose package (both with and without underscore)
    SKIP_PREFIXES = (
        "U_", "@", "#", "EUR", "CP_", "MRK_", "SBO_", "BEM", "CFDI",
        "ERPN", "EDF", "ECM", "BIP", "KP_", "POS_", "VM_", " CEST", "CEST",
        "CRM_"
    )

    upper_name = name.upper()
    if any(upper_name.startswith(p) for p in SKIP_PREFIXES):
        # Specific exception list: things that start with these letters but ARE SAP Standard
        # Add here if anything is wrongly skipped
        pass
        return True

    # Also ignore anything that has _U_ in the middle (common in some developments)
    if "_U_" in name:
        return True

    # Standard noisy fields
    return name in ("Validations", "UserFields")


class MetadataParser:
    def __init__(self, xml_path: str | Path):
        self.path = Path(xml_path)
        self.ns = self._detect_namespace()

    def _detect_namespace(self) -> dict[str, str]:
        with open(self.path, encoding="utf-8") as f:
            header = f.read(2048)
        if "oasis-open.org" in header:
            return NS
        return NS_LEGACY

    def parse(self, xml_path: str | None = None, service_doc_path: str | None = None, ref_cache_path: str | None = None) -> ParsedMetadata:
        # Load filtering data if available
        service_doc = []
        if service_doc_path and Path(service_doc_path).exists():
            print(f"Loading Service Document filter: {service_doc_path}")
            with open(service_doc_path, 'r') as f:
                doc = json.load(f)
                service_doc = [v["name"] for v in doc.get("value", [])]

        ref_cache = {}
        if ref_cache_path and Path(ref_cache_path).exists():
            print(f"Loading Reference Cache enrichment: {ref_cache_path}")
            with open(ref_cache_path, 'r') as f:
                ref_cache = json.load(f)

        metadata = ParsedMetadata(service_document=service_doc, reference_cache=ref_cache)

        path_to_parse = xml_path if xml_path else self.path
        context = ET.iterparse(path_to_parse, events=("start", "end"))
        current_entity: SAPEntityType | None = None
        current_complex: SAPComplexType | None = None
        current_enum: SAPEnumType | None = None

        edm_ns = self.ns["edm"]

        for event, elem in context:
            tag = elem.tag.replace(f"{{{edm_ns}}}", "")

            if event == "start":
                if tag == "EntityType":
                    name = elem.get("Name", "")
                    if not _should_skip(name):
                        current_entity = SAPEntityType(
                            name=name,
                            service_name=name,
                        )
                        current_complex = None
                elif tag == "ComplexType":
                    name = elem.get("Name", "")
                    if not _should_skip(name):
                        current_complex = SAPComplexType(name=name)
                        current_entity = None
                elif tag == "EnumType":
                    name = elem.get("Name", "")
                    if not _should_skip(name):
                        current_enum = SAPEnumType(name=name)
                elif tag == "Property":
                    name = elem.get("Name", "")
                    edm_type = elem.get("Type", "Edm.String")
                    nullable = elem.get("Nullable", "true").lower() == "true"
                    if _should_skip(name):
                        continue
                    prop = SAPProperty(name=name, edm_type=edm_type, nullable=nullable)
                    if current_entity:
                        current_entity.properties.append(prop)
                    elif current_complex:
                        current_complex.properties.append(prop)
                elif tag == "NavigationProperty" and current_entity:
                    nav_name = elem.get("Name", "")
                    if not _should_skip(nav_name):
                        target = elem.get("Type", "")
                        if target.startswith("Collection("):
                            multiplicity = "*"
                            target = target[11:-1]
                        else:
                            multiplicity = "0..1"
                        target_clean = target.split(".")[-1]
                        current_entity.nav_properties.append(
                            SAPNavigationProperty(
                                name=nav_name,
                                target_type=target_clean,
                                multiplicity=multiplicity,
                            )
                        )
                elif tag == "PropertyRef" and current_entity:
                    key_name = elem.get("Name", "")
                    if key_name:
                        current_entity.key_properties.append(key_name)
                elif tag == "Member" and current_enum:
                    member_name = elem.get("Name", "")
                    member_value = int(elem.get("Value", "0"))
                    if not _should_skip(member_name):
                        current_enum.members.append(
                            SAPEnumMember(name=member_name, value=member_value)
                        )
                elif tag == "EntitySet":
                    name = elem.get("Name", "")
                    if _should_skip(name): continue

                    # --- FILTRO VANILLA & DOC PRIORITY ---
                    # 1. DOCUMENTATION PRIORITY: Only include if in reference_cache
                    if metadata.reference_cache and name not in metadata.reference_cache:
                        # Skip undocumented objects to avoid internal garbage
                        continue

                    # 2. Reject if not in the active service document (if provided)
                    if metadata.service_document and name not in metadata.service_document:
                        continue

                    # 3. Enrichment from reference
                    ref_info = metadata.reference_cache.get(name, {})

                    entity_type = elem.get("EntityType", "")
                    if name and entity_type:
                        clean_type = entity_type.split(".")[-1]
                        metadata.entity_sets[name] = SAPEntitySet(
                            name=name,
                            entity_type=clean_type,
                            description=ref_info.get("description", "")
                        )
                elif tag in ("Action", "Function", "ActionImport", "FunctionImport"):
                    name = elem.get("Name", "")
                    if not name or _should_skip(name): continue

                    # 1. DOCUMENTATION PRIORITY
                    if metadata.reference_cache:
                        # For actions like ServiceName_Action, check if ServiceName is in cache
                        potential_service = name.split("_")[0] if "_" in name else name
                        if potential_service not in metadata.reference_cache and name not in metadata.reference_cache:
                            # Also check if it belongs to a known EntitySet that is in cache
                            # (Some bound actions don't have the service prefix)
                            is_in_cache = False
                            for top_level in metadata.reference_cache.values():
                                if name in top_level: # It's an operation inside a service
                                    is_in_cache = True
                                    break
                            if not is_in_cache:
                                continue
                    is_bound = elem.get("IsBound", "false").lower() == "true"
                    bound_type = None
                    if is_bound:
                        param = elem.find("{*}Parameter")
                        if param is not None:
                            bound_type = param.get("Type", "").split(".")[-1]

                    entity_set = elem.get("EntitySet", "")

                    if tag.startswith("Action"):
                        act_func = ActionDef(name=name, bound_entity_set=entity_set, is_bound=is_bound, bound_type=bound_type)
                    else:
                        act_func = FunctionDef(name=name, bound_entity_set=entity_set, is_bound=is_bound, bound_type=bound_type) # type: ignore

                    # Group actions into 'Dedicated Services' if they follow the ServiceName_Action pattern
                    if "_" in name and not is_bound:
                        service_name = name.split("_")[0]
                        # Clean name to see if it matches an existing entity set
                        # e.g. ActivitiesService -> Activities
                        clean_target_name = service_name
                        if service_name.endswith("Service"):
                             clean_target_name = service_name[:-7]

                        target_es = None
                        # DECISION: Should we merge into EntitySet or keep as Dedicated Service?
                        # If the service_name itself is a documented entity in reference_cache,
                        # we keep it separate as a Dedicated Service.
                        if service_name in metadata.reference_cache:
                            # Keep as Dedicated Service
                            target_es = None
                        elif clean_target_name in metadata.entity_sets:
                             target_es = metadata.entity_sets[clean_target_name]
                        elif service_name in metadata.entity_sets:
                             target_es = metadata.entity_sets[service_name]

                        if target_es:
                             # Merge into existing EntitySet
                             if tag.startswith("Action"):
                                 if not any(a.name == name for a in target_es.actions):
                                     target_es.actions.append(act_func) # type: ignore
                             else:
                                 if not any(f.name == name for f in target_es.functions):
                                     target_es.functions.append(act_func) # type: ignore
                        else:
                             # Create/Find a Dedicated Service
                             if service_name not in metadata.dedicated_services:
                                 metadata.dedicated_services[service_name] = SAPEntitySet(
                                     name=service_name,
                                     entity_type="None",
                                 )
                             target_service = metadata.dedicated_services[service_name]
                             if tag.startswith("Action"):
                                 if not any(a.name == name for a in target_service.actions):
                                     target_service.actions.append(act_func) # type: ignore
                             else:
                                 if not any(f.name == name for f in target_service.functions):
                                     target_service.functions.append(act_func) # type: ignore

                    if tag.startswith("Action"):
                         metadata.raw_actions.append(act_func) # type: ignore
                         if entity_set in metadata.entity_sets:
                             metadata.entity_sets[entity_set].actions.append(act_func) # type: ignore
                    else:
                         metadata.raw_functions.append(act_func) # type: ignore
                         if entity_set in metadata.entity_sets:
                             metadata.entity_sets[entity_set].functions.append(act_func) # type: ignore
            elif event == "end":
                if tag == "EntityType" and current_entity:
                    metadata.entities[current_entity.name] = current_entity
                    current_entity = None
                elif tag == "ComplexType" and current_complex:
                    metadata.complex_types[current_complex.name] = current_complex
                    current_complex = None
                elif tag == "EnumType" and current_enum:
                    metadata.enums[current_enum.name] = current_enum
                    current_enum = None
            elem.clear()
        return metadata
