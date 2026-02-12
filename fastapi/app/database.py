import pandas as pd
import os
from typing import List, Dict, Any, Optional

class Database:
    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        if os.path.exists(csv_path):
            self.df = pd.read_csv(csv_path)
            # Add an internal index if not present
            self.df['id'] = range(len(self.df))
        else:
            self.df = pd.DataFrame()

    def get_bookings(self, 
                     filters: Dict[str, Any] = None, 
                     fields: List[str] = None, 
                     page: int = 1, 
                     size: int = 10) -> Dict[str, Any]:
        
        filtered_df = self.df.copy()
        
        # Apply filters
        if filters:
            for key, value in filters.items():
                if key in filtered_df.columns and value is not None:
                    filtered_df = filtered_df[filtered_df[key] == value]
        
        total = len(filtered_df)
        start = (page - 1) * size
        end = start + size
        
        paginated_df = filtered_df.iloc[start:end]
        
        # Select fields
        if fields:
            # Ensure 'id' is always included or at least handle it
            valid_fields = [f for f in fields if f in paginated_df.columns]
            if valid_fields:
                paginated_df = paginated_df[valid_fields]
        
        data = paginated_df.to_dict(orient='records')
        
        next_page_token = str(page + 1) if end < total else None
        
        return {
            "data": data,
            "total": total,
            "page": page,
            "size": size,
            "next_page_token": next_page_token
        }

    def add_booking(self, booking_data: Dict[str, Any]) -> Dict[str, Any]:
        new_id = self.df['id'].max() + 1 if not self.df.empty else 0
        booking_data['id'] = new_id
        new_row = pd.DataFrame([booking_data])
        self.df = pd.concat([self.df, new_row], ignore_index=True)
        return booking_data

    def update_booking(self, booking_id: int, booking_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if booking_id not in self.df['id'].values:
            return None
        
        idx = self.df.index[self.df['id'] == booking_id].tolist()[0]
        for key, value in booking_data.items():
            if key in self.df.columns and value is not None:
                self.df.at[idx, key] = value
        
        return self.df.iloc[idx].to_dict()

# Initialize database
CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "hotel_bookings.csv")
db = Database(CSV_PATH)
