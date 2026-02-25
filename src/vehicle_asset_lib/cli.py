import typer
import json
import os
from datetime import datetime
from typing import Optional, List
from dotenv import load_dotenv
from .db import SessionLocal, init_db
from .services.verification import VerificationService
from .services.assets import AssetService
from .services.admin import AdminService
from .services.auth import validate_admin_secret
from .models import AssetType

# Load environment variables
load_dotenv()

app = typer.Typer()

@app.command()
def verify(name: str, id_digits: str):
    with SessionLocal() as db:
        service = VerificationService(db)
        result = service.verify_user(name, id_digits)
        typer.echo(json.dumps(result))

@app.command()
def list(type: str = "all"):
    with SessionLocal() as db:
        service = AssetService(db)
        result = service.list_assets(type)
        typer.echo(json.dumps(result))

@app.command()
def loans():
    with SessionLocal() as db:
        service = AssetService(db)
        result = service.list_active_loans()
        typer.echo(json.dumps(result))

@app.command()
def pickup(user_id: str, asset_ids: str):
    ids = [aid.strip() for aid in asset_ids.split(",")]
    with SessionLocal() as db:
        service = AssetService(db)
        result = service.pickup(user_id, ids)
        typer.echo(json.dumps(result))

@app.command(name="return")
def return_command(user_id: str, asset_ids: str):
    ids = [aid.strip() for aid in asset_ids.split(",")]
    with SessionLocal() as db:
        service = AssetService(db)
        result = service.return_assets(user_id, ids)
        typer.echo(json.dumps(result))

@app.command()
def notify_admins(dry_run: bool = typer.Option(False, "--dry-run", help="Scan for warnings and print without sending email"), json_out: bool = typer.Option(False, "--json", help="Output results in JSON format")):
    from .services.monitoring import MonitoringService
    from .services.notifications import EmailService
    import json as json_lib
    
    with SessionLocal() as db:
        monitoring = MonitoringService(db)
        alerts = monitoring.check_vehicle_alerts()
        
        if not alerts:
            if json_out:
                typer.echo(json_lib.dumps([]))
            else:
                typer.echo("No vehicle warnings detected. No email sent.")
            return

        if dry_run:
            if json_out:
                typer.echo(json_lib.dumps(alerts))
            else:
                typer.echo(f"[DRY RUN] Would send following warnings to {os.getenv('ADMIN_NOTIFICATION_EMAIL')}:")
                for alert in alerts:
                    typer.echo(f"- {alert['identifier']}: {alert['status']} (Last/Exp: {alert['date']})")
            return
            
        email_service = EmailService()
        success = email_service.send_admin_alert(alerts)
        
        if json_out:
            typer.echo(json_lib.dumps({"sent": success, "alerts": alerts}))
        else:
            if success:
                typer.echo(f"Sent notification email to {email_service.admin_email} containing {len(alerts)} warnings.")
            else:
                typer.echo("Failed to send notification email.", err=True)

admin_app = typer.Typer()
app.add_typer(admin_app, name="admin")

@admin_app.callback()
def admin_auth():
    """
    Security check for all admin commands.
    """
    secret = os.getenv("ADMIN_SECRET")
    if not validate_admin_secret(secret):
        typer.echo("Error: [Access Denied] Missing or invalid ADMIN_SECRET.", err=True)
        raise typer.Exit(code=1)

@admin_app.command()
def init():
    init_db()
    typer.echo("Database initialized.")

@admin_app.command()
def add_asset(
    type: str, 
    identifier: str,
    maintenance_date: Optional[datetime] = typer.Option(None, formats=["%Y-%m-%d", "%Y-%m-%dT%H:%M:%S"]),
    maintenance_mileage: Optional[int] = None,
    inspection_date: Optional[datetime] = typer.Option(None, formats=["%Y-%m-%d", "%Y-%m-%dT%H:%M:%S"]),
    insurance_date: Optional[datetime] = typer.Option(None, formats=["%Y-%m-%d", "%Y-%m-%dT%H:%M:%S"])
):
    with SessionLocal() as db:
        service = AdminService(db)
        asset_type = AssetType.KEY if type.upper() == "KEY" else AssetType.GAS_CARD
        asset = service.add_asset(
            asset_type, 
            identifier,
            maintenance_date=maintenance_date,
            maintenance_mileage=maintenance_mileage,
            inspection_date=inspection_date,
            insurance_date=insurance_date
        )
        result = {"id": str(asset.id), "identifier": asset.identifier, "type": asset.type.value}
        if asset.type == AssetType.KEY:
            result.update({
                "maintenance_date": asset.maintenance_date.isoformat() if asset.maintenance_date else None,
                "maintenance_mileage": asset.maintenance_mileage,
                "inspection_date": asset.inspection_date.isoformat() if asset.inspection_date else None,
                "insurance_date": asset.insurance_date.isoformat() if asset.insurance_date else None,
            })
        typer.echo(json.dumps(result))

@admin_app.command()
def update_asset(
    asset_id: str, 
    identifier: Optional[str] = None, 
    type: Optional[str] = None,
    maintenance_date: Optional[datetime] = typer.Option(None, formats=["%Y-%m-%d", "%Y-%m-%dT%H:%M:%S"]),
    maintenance_mileage: Optional[int] = None,
    inspection_date: Optional[datetime] = typer.Option(None, formats=["%Y-%m-%d", "%Y-%m-%dT%H:%M:%S"]),
    insurance_date: Optional[datetime] = typer.Option(None, formats=["%Y-%m-%d", "%Y-%m-%dT%H:%M:%S"])
):
    with SessionLocal() as db:
        service = AdminService(db)
        asset_type = None
        if type:
            asset_type = AssetType.KEY if type.upper() == "KEY" else AssetType.GAS_CARD
        
        asset = service.update_asset(
            asset_id, 
            identifier=identifier, 
            type=asset_type,
            maintenance_date=maintenance_date,
            maintenance_mileage=maintenance_mileage,
            inspection_date=inspection_date,
            insurance_date=insurance_date
        )
        if asset:
            result = {
                "id": str(asset.id), 
                "identifier": asset.identifier, 
                "type": asset.type.value
            }
            if asset.type == AssetType.KEY:
                result.update({
                    "maintenance_date": asset.maintenance_date.isoformat() if asset.maintenance_date else None,
                    "maintenance_mileage": asset.maintenance_mileage,
                    "inspection_date": asset.inspection_date.isoformat() if asset.inspection_date else None,
                    "insurance_date": asset.insurance_date.isoformat() if asset.insurance_date else None,
                })
            typer.echo(json.dumps(result))
        else:
            typer.echo("Asset not found", err=True)

@admin_app.command()
def delete_asset(asset_id: str):
    with SessionLocal() as db:
        service = AdminService(db)
        if service.delete_asset(asset_id):
            typer.echo("Asset deleted")
        else:
            typer.echo("Asset not found", err=True)

@admin_app.command()
def add_user(name: str, id_last4: str):
    with SessionLocal() as db:
        service = AdminService(db)
        user = service.add_user(name, id_last4)
        typer.echo(json.dumps({"id": str(user.id), "name": user.name}))

@admin_app.command()
def list_users():
    with SessionLocal() as db:
        service = AdminService(db)
        users = service.list_users()
        result = [{"id": str(u.id), "name": u.name, "id_last4": u.id_last4, "status": u.status.value} for u in users]
        typer.echo(json.dumps(result))

@admin_app.command()
def update_user(user_id: str, name: Optional[str] = None, id_last4: Optional[str] = None):
    with SessionLocal() as db:
        service = AdminService(db)
        user = service.update_user(user_id, name=name, id_last4=id_last4)
        if user:
            typer.echo(json.dumps({"id": str(user.id), "name": user.name}))
        else:
            typer.echo("User not found", err=True)

@admin_app.command()
def delete_user(user_id: str):
    with SessionLocal() as db:
        service = AdminService(db)
        if service.delete_user(user_id):
            typer.echo("User deleted")
        else:
            typer.echo("User not found", err=True)

@admin_app.command()
def seed_otps(file_path: Optional[str] = None, count: int = 100):
    passwords = []
    if file_path:
        with open(file_path, "r") as f:
            passwords = [line.strip() for line in f if line.strip()]
    else:
        # Generate some mock OTPs if no file provided
        passwords = [f"OTP-{i:04d}" for i in range(count)]
        
    with SessionLocal() as db:
        service = AdminService(db)
        result = service.seed_otps(passwords)
        typer.echo(json.dumps(result))

if __name__ == "__main__":
    app()
