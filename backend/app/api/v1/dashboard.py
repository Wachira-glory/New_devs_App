from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
from app.services.cache import get_revenue_summary
from app.core.auth import authenticate_request as get_current_user

router = APIRouter()

@router.get("/dashboard/summary")
async def get_dashboard_summary(
    property_id: str,
    current_user: dict = Depends(get_current_user)
) -> Dict[str, Any]:
    
    ##I switched from using default ID to the user's company ID, 
    ##because that was accidentally showing Client's A data to Client B
    tenant_id=current_user.get("tenant_id")
    # If the user is not known then stop them here for safety.
    if not tenant_id:
        raise HTTPException(status_code=403,detail="The Tenant ID is missing.")
    
    # Get the money data using the correct Company ID.
    revenue_data = await get_revenue_summary(property_id, tenant_id)
    
    # Here, I fixed the "cents" issue to show exactly two decimal places.
    total_revenue_number = round(float(revenue_data['total']),2)
    
    return {
        "property_id": revenue_data['property_id'],
        "total_revenue": total_revenue_number,
        "currency": revenue_data['currency'],
        "reservations_count": revenue_data['count']
    }
