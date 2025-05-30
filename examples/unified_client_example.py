#!/usr/bin/env python3
"""
Unified KytheraKdx Client Example

This example demonstrates how to use the unified KytheraKdx client
to access all Kythera API functionality through a single entry point.
"""

from kythera_kdx import KytheraKdx, KytheraAPIError, KytheraAuthError
from datetime import date
import pandas as pd
import os

def main():
    """Main example function demonstrating unified client usage."""
    
    # Initialize the unified client
    # You can use environment variables or pass credentials directly
    kdx = KytheraKdx(
        client_id=os.getenv("KYTHERA_CLIENT_ID", "your-client-id"),
        client_secret=os.getenv("KYTHERA_CLIENT_SECRET", "your-client-secret"),
        tenant_id=os.getenv("KYTHERA_TENANT_ID", "your-tenant-id")
    )
    
    try:
        print("🚀 Kythera KDX Unified Client Example")
        print("=" * 50)
        
        # Example 1: Get fund information
        print("\n📊 1. Fetching Fund Information")
        funds = kdx.funds.get_funds(enabled_only=True)
        print(f"   Found {len(funds)} active funds")
        
        if funds:
            fund = funds[0]
            print(f"   Sample Fund: {fund.fullName} ({fund.shortName})")
            
            # Get NAVs for this fund
            navs = kdx.funds.get_fund_navs(date=date.today(), fund_id=fund.id)
            if navs:
                print(f"   Current NAV: {navs[0].value:.2f}")
        
        # Example 2: Get current positions
        print("\n💼 2. Fetching Current Positions")
        positions = kdx.positions.get_positions(is_open=True)
        print(f"   Found {len(positions)} open positions")
        
        if positions:
            # Get as DataFrame for analysis
            positions_df = kdx.positions.get_positions_df(is_open=True)
            total_market_value = positions_df['marketValue'].sum()
            print(f"   Total Market Value: ${total_market_value:,.2f}")
        
        # Example 3: Get current P&L
        print("\n📈 3. Analyzing Current P&L")
        pnl_df = kdx.pnl.get_intraday_pnl_df()
        
        if not pnl_df.empty:
            total_pnl = pnl_df['pnl'].sum()
            print(f"   Total Intraday P&L: ${total_pnl:,.2f}")
            
            # Top and bottom performers
            top_performer = pnl_df.loc[pnl_df['pnl'].idxmax()]
            bottom_performer = pnl_df.loc[pnl_df['pnl'].idxmin()]
            
            print(f"   Best Performer: {top_performer['instrumentName']} (${top_performer['pnl']:,.2f})")
            print(f"   Worst Performer: {bottom_performer['instrumentName']} (${bottom_performer['pnl']:,.2f})")
        
        # Example 4: Get market prices
        print("\n💰 4. Fetching Market Prices")
        try:
            prices_df = kdx.prices.get_all_prices_df(
                price_date=date.today(),
                price_type_name="CLOSE"
            )
            print(f"   Found prices for {len(prices_df)} instruments")
        except Exception as e:
            print(f"   Note: Price data may not be available: {e}")
        
        # Example 5: Get real-time data
        print("\n⚡ 5. Fetching Intraday Data")
        try:
            intraday_prices = kdx.intraday.get_intraday_prices()
            print(f"   Found {len(intraday_prices)} real-time prices")
        except Exception as e:
            print(f"   Note: Intraday data may not be available: {e}")
        
        # Example 6: Get trading activity
        print("\n🔄 6. Fetching Today's Trades")
        try:
            trades = kdx.trades.get_trades(effective_date=date.today())
            print(f"   Found {len(trades)} trades today")
            
            if trades:
                trades_df = kdx.trades.get_trades_df(effective_date=date.today())
                total_volume = trades_df['notional'].sum()
                print(f"   Total Trading Volume: ${total_volume:,.2f}")
        except Exception as e:
            print(f"   Note: Trade data may not be available: {e}")
        
        # Example 7: Get reference data
        print("\n🌍 7. Fetching Reference Data")
        try:
            currencies = kdx.globals.get_currencies()
            print(f"   Found {len(currencies)} currencies")
            
            countries = kdx.globals.get_countries()
            print(f"   Found {len(countries)} countries")
        except Exception as e:
            print(f"   Note: Reference data may not be available: {e}")
        
        print("\n✅ Example completed successfully!")
        print("\n💡 Pro Tips:")
        print("   - Use the _df() methods to get pandas DataFrames for analysis")
        print("   - Use the _raw() methods to get raw JSON data")
        print("   - Regular methods return typed objects with full IntelliSense support")
        print("   - All methods support the same parameters as individual client classes")
        
    except KytheraAuthError as e:
        print(f"❌ Authentication Error: {e}")
        print("   Check your client_id, client_secret, and tenant_id")
        
    except KytheraAPIError as e:
        print(f"❌ API Error: {e.status_code} - {e}")
        print("   Check the API documentation for valid parameters")
        
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")

if __name__ == "__main__":
    main()
