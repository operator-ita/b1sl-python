
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup
from dataclasses import dataclass, field
from typing import Dict, List, Optional

@dataclass
class MethodInfo:
    name: str
    verb: str
    description: str = ""
    example_payload: Optional[str] = None

@dataclass
class ServiceReference:
    name: str
    description: str = ""
    methods: Dict[str, MethodInfo] = field(default_factory=dict)

class SAPReferenceParser:
    def __init__(self, html_path: str):
        self.html_path = Path(html_path)
        self.services: Dict[str, ServiceReference] = {}

    def parse(self) -> Dict[str, ServiceReference]:
        if not self.html_path.exists():
            print(f"Reference file {self.html_path} not found.")
            return {}

        print(f"Parsing SAP API Reference: {self.html_path}...")
        with open(self.html_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')

        # SAP Reference uses <li class="resource"> for each service
        resources = soup.find_all('li', class_='resource')
        for res in resources:
            try:
                # 1. Service Name (h2)
                h2 = res.find('h2')
                if not h2: continue
                service_name = h2.get_text(strip=True)
                
                # 2. Service Description
                methods_div = res.find('div', class_='methods')
                if not methods_div: continue
                
                desc_p = methods_div.find('p')
                service_desc = desc_p.get_text(strip=True) if desc_p else ""
                
                service_ref = ServiceReference(name=service_name, description=service_desc)
                
                # 3. Parse Methods (<div class="method">)
                for method_div in methods_div.find_all('div', class_='method'):
                    path_span = method_div.find('span', class_='path')
                    verb_span = method_div.find('span', class_='http_method')
                    
                    if not path_span or not verb_span: continue
                    
                    method_name = path_span.get_text(strip=True)
                    http_verb = verb_span.get_text(strip=True)
                    
                    # Method detail description
                    content_div = method_div.find('div', class_='content')
                    method_desc = ""
                    example_json = None
                    
                    if content_div:
                        method_p = content_div.find('p')
                        if method_p:
                            method_desc = method_p.get_text(strip=True)
                        
                        # Extract Example JSON
                        pre_tag = content_div.find('pre')
                        if pre_tag:
                            text = pre_tag.get_text()
                            # Clean up example URL and find JSON block
                            json_match = re.search(r'(\{.*\})', text, re.DOTALL)
                            if json_match:
                                example_json = json_match.group(1).strip()

                    service_ref.methods[method_name] = MethodInfo(
                        name=method_name,
                        verb=http_verb,
                        description=method_desc,
                        example_payload=example_json
                    )
                
                self.services[service_name] = service_ref
                
            except Exception as e:
                print(f"Warning: Failed to parse a resource in HTML: {e}")

        print(f"Successfully extracted {len(self.services)} standard services from reference.")
        return self.services

    def save_cache(self, output_path: str):
        """Saves a simplified JSON version for faster generation cycles."""
        data = {
            name: {
                "description": s.description,
                "methods": {
                    m_name: {
                        "verb": m.verb,
                        "description": m.description,
                        "example": m.example_payload
                    } for m_name, m in s.methods.items()
                }
            } for name, s in self.services.items()
        }
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python scripts/sap_metadata_generator/reference_parser.py <html_path> <cache_output_path>")
        sys.exit(1)
        
    html_input = sys.argv[1]
    cache_output = sys.argv[2]
    
    parser = SAPReferenceParser(html_input)
    parser.parse()
    parser.save_cache(cache_output)
