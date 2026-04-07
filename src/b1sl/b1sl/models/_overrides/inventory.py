from .._generated.entities.inventory import Item as _Item


class Item(_Item):
    """
    Manual override for Item entity to add business logic.
    """

    @property
    def available_stock(self) -> float:
        """
        Calculated available stock based on standard SAP logic:
        Available = OnHand - IsCommited + OnOrder

        Mapping:
        - OnHand: quantity_on_stock
        - IsCommited: quantity_ordered_by_customers
        - OnOrder: quantity_ordered_from_vendors
        """
        on_hand = self.quantity_on_stock or 0.0
        committed = self.quantity_ordered_by_customers or 0.0
        ordered = self.quantity_ordered_from_vendors or 0.0

        return on_hand - committed + ordered
