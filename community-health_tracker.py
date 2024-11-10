import os
import json
from datetime import datetime
import time
import sys

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

class AdvancedHealthTracker:
    def _init_(self):
        """Initialize the tracker with necessary files and data structures."""
        self.users_file = "users.json"
        self.health_data_file = "health_data.json"
        self.ensure_data_files()
        self.users = self.load_data(self.users_file)
        self.health_data = self.load_data(self.health_data_file)
        self.initialize_health_tips()

    def ensure_data_files(self):
        """Ensure data files exist with valid JSON."""
        for file in [self.users_file, self.health_data_file]:
            if not os.path.exists(file):
                with open(file, 'w') as f:
                    json.dump({}, f)

    def load_data(self, filename):
        """Load data from JSON file."""
        try:
            if os.path.exists(filename):
                with open(filename, 'r') as f:
                    return json.load(f)
            return {}
        except:
            return {}

    def save_data(self, data, filename):
        """Save data to JSON file."""
        try:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=4)
            return True
        except:
            return False

    def print_slowly(self, text, delay=0.05):
        """Print text with a typing effect."""
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()

    def display_welcome_message(self):
        """Display an enhanced interactive welcome message."""
        clear_screen()
        
        print("\n" + "═" * 70)
        print("║" + " " * 20 + "COMMUNITY HEALTH TRACKER" + " " * 20 + "║")
        print("═" * 70 + "\n")
        
        welcome_messages = [
            "🌟 Welcome to Your Personal Health Management System! 🌟",
            "\nAbout Our Application:",
            "We help you maintain and improve your health through:",
            "\n🏥 Health Monitoring & Tracking",
            "   • Log your daily health metrics",
            "   • Monitor weight, blood pressure, and activity",
            "   • View your health history",
            "\n💪 Personalized Health Advice",
            "   • Get customized health tips",
            "   • Receive symptom-specific advice",
            "   • Access health recommendations",
            "\n📊 Features Available:",
            "   • User Registration and Login",
            "   • Health Metrics Logging",
            "   • Health Tips and Advice",
            "   • Personal Health History",
            "   • Progress Tracking"
        ]
        
        for message in welcome_messages:
            self.print_slowly(message, 0.03)
        
        print("\nLoading your health companion", end='')
        for _ in range(3):
            time.sleep(0.5)
            print(".", end='', flush=True)
        print("\n")
        
        input("Press Enter to begin your health journey...")
        clear_screen()

    def initialize_health_tips(self):
        """Initialize health tips database."""
        self.health_tips = {
            "general": [
                "Stay hydrated by drinking at least 8 glasses of water daily",
                "Aim for 7-9 hours of sleep each night",
                "Practice good posture throughout the day",
                "Take regular breaks from screen time",
                "Stay socially connected with friends and family"
            ],
            "nutrition": [
                "Include a variety of fruits and vegetables in your diet",
                "Choose whole grains over refined grains",
                "Limit processed foods and added sugars",
                "Eat protein-rich foods with each meal",
                "Practice mindful eating",
                "Plan your meals ahead"
            ],
            "exercise": [
                "Aim for 30 minutes of moderate exercise daily",
                "Include both cardio and strength training",
                "Take regular walking breaks",
                "Try different types of physical activities",
                "Start with gentle exercises if you're new to working out",
                "Remember to stretch before and after exercise"
            ]
        }

    def register_user(self, username):
        """Register a new user."""
        if not username or len(username) < 3:
            return False, "Username must be at least 3 characters long!"
        
        if username in self.users:
            return False, "Username already exists!"
        
        self.users[username] = {
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        if self.save_data(self.users, self.users_file):
            return True, "Registration successful!"
        return False, "Error saving user data!"

    def log_health_metrics(self, username, weight, blood_pressure, steps):
        """Log user's health metrics."""
        try:
            weight = float(weight)
            steps = int(steps)
            
            # Validate blood pressure format
            if not blood_pressure.count('/') == 1:
                return False, "Blood pressure must be in format '120/80'"
            
            sys_bp, dia_bp = map(int, blood_pressure.split('/'))
            if not (60 <= sys_bp <= 200 and 40 <= dia_bp <= 130):
                return False, "Blood pressure values are out of normal range"
            
            if username not in self.health_data:
                self.health_data[username] = []
            
            entry = {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "weight": weight,
                "blood_pressure": blood_pressure,
                "steps": steps
            }
            
            self.health_data[username].append(entry)
            if self.save_data(self.health_data, self.health_data_file):
                return True, "Health metrics logged successfully!"
            return False, "Error saving health data!"
        except ValueError:
            return False, "Please enter valid numbers!"
        except Exception as e:
            return False, f"Error: {str(e)}"

    def get_health_tips(self, category="general"):
        """Get health tips by category."""
        return self.health_tips.get(category, self.health_tips["general"])

    def display_health_history(self, username):
        """Display user's health history."""
        if username not in self.health_data or not self.health_data[username]:
            print("\nNo health data recorded yet.")
            return
        
        print("\nYour Health History:")
        print("-" * 80)
        print(f"{'Date':<25} {'Weight (kg)':<15} {'Blood Pressure':<15} {'Steps':<10}")
        print("-" * 80)
        
        for entry in self.health_data[username]:
            print(f"{entry['date']:<25} {entry['weight']:<15.1f} {entry['blood_pressure']:<15} {entry['steps']:<10}")

    def analyze_health_metrics(self, username):
        """Analyze user's health metrics and provide insights."""
        if username not in self.health_data or not self.health_data[username]:
            return "No health data available for analysis."
        
        data = self.health_data[username]
        latest = data[-1]  # Most recent entry
        
        insights = [
            "\n=== Health Metrics Analysis ===",
            f"\nLatest Measurements (Date: {latest['date']}):",
            f"Weight: {latest['weight']:.1f} kg",
            f"Blood Pressure: {latest['blood_pressure']}",
            f"Steps: {latest['steps']:,}",
            "\nRecommendations:",
            "• Maintain regular monitoring of your health metrics",
            "• Consult healthcare provider for professional advice",
            "• Keep up with your health tracking routine"
        ]
        
        return "\n".join(insights)

def main():
    """Main application function."""
    tracker = AdvancedHealthTracker()
    current_user = None
    
    tracker.display_welcome_message()
    
    while True:
        try:
            print("\n=== Community Health Tracker ===")
            if current_user:
                print(f"Logged in as: {current_user}")
            
            print("\n1. Register")
            print("2. Login")
            print("3. Log Health Metrics")
            print("4. View Health Tips")
            print("5. View Health History")
            print("6. Exit")
            
            choice = input("\nEnter your choice (1-6): ").strip()
            
            if choice == "1":  # Register
                username = input("Enter username for registration: ").strip()
                if username in tracker.users:
                    print(f"\n❌ Username '{username}' already exists. Please choose a different username or login instead.")
                else:
                    success, message = tracker.register_user(username)
                    if success:
                        print(f"\n✅ Registration successful! Welcome, {username}!")
                        current_user = username
                    else:
                        print(f"\n❌ Registration failed: {message}")

            elif choice == "2":  # Login
                username = input("Enter username to login: ").strip()
                if username in tracker.users:
                    print(f"\n✅ Login successful! Welcome back, {username}!")
                    current_user = username
                else:
                    print(f"\n❌ Username '{username}' not found. Please register first.")

            elif choice == "3":  # Log Health Metrics
                if not current_user:
                    print("\n❌ Please login first to log health metrics.")
                else:
                    print("\n=== Health Metrics Logging ===")
                    print("Why track these metrics?")
                    print("• Weight: Monitor your progress and maintain a healthy range")
                    print("• Blood Pressure: Track cardiovascular health")
                    print("• Steps: Measure daily physical activity level")
                    
                    weight = input("\nEnter weight (kg): ").strip()
                    bp = input("Enter blood pressure (e.g., 120/80): ").strip()
                    steps = input("Enter steps walked today: ").strip()
                    
                    success, message = tracker.log_health_metrics(current_user, weight, bp, steps)
                    if success:
                        print(f"\n✅ {message}")
                        analysis = tracker.analyze_health_metrics(current_user)
                        print(analysis)
                    else:
                        print(f"\n❌ {message}")

            elif choice == "4":  # View Health Tips
                while True:
                    print("\n=== Health Tips Categories ===")
                    print("1. General Health")
                    print("2. Nutrition")
                    print("3. Exercise")
                    print("4. Return to Main Menu")
                    
                    tip_choice = input("\nSelect category (1-4): ").strip()
                    
                    if tip_choice == "4":
                        break
                        
                    category_map = {
                        "1": "general",
                        "2": "nutrition",
                        "3": "exercise"
                    }
                    
                    if tip_choice in category_map:
                        tips = tracker.get_health_tips(category_map[tip_choice])
                        print(f"\n{category_map[tip_choice].title()} Tips:")
                        i = 0
                        while i < len(tips):
                            print(f"\n{i + 1}. {tips[i]}")
                            if i < len(tips) - 1:
                                print("\nOptions:")
                                print("1. Next tip")
                                print("2. Exit to categories")
                                
                                next_choice = input("\nEnter your choice (1-2): ").strip()
                                if next_choice == "1":
                                    i += 1
                                elif next_choice == "2":
                                    break
                                else:
                                    print("\n❌ Invalid choice. Please enter 1 or 2.")
                            else:
                                print("\nEnd of tips for this category.")
                                input("\nPress Enter to return to categories...")
                                break
                    else:
                        print("\n❌ Invalid category choice.")

            elif choice == "5":  # View Health History
                if not current_user:
                    print("\n❌ Please login first to view health history.")
                else:
                    tracker.display_health_history(current_user)

            elif choice == "6":  # Exit
                print("\n👋 Thank you for using the Community Health Tracker! Stay healthy!")
                break

            else:
                print("\n❌ Invalid choice. Please enter a number between 1 and 6.")

            if choice != "4":  # Don't clear screen when viewing tips
                input("\nPress Enter to continue...")
                clear_screen()

        except KeyboardInterrupt:
            print("\n\nReturning to main menu...")
        except Exception as e:
            print(f"\n❌ An error occurred: {str(e)}")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()