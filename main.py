import os
import subprocess


def list_phones_and_apps():
    """Lists the phone models in the 'phones' directory and their associated apps to be deleted."""

    phone_dir = "phones"
    phone_files = [f for f in os.listdir(phone_dir) if f.endswith(".txt")]

    if not phone_files:
        print("No phone models found in the 'phones' directory.")
        return

    print("Available phone models:")
    for i, phone_file in enumerate(phone_files, 1):
        print(f"{i}. {phone_file}")

    while True:
        try:
            choice = int(input("Enter the number of the phone model you want to process: "))
            if 1 <= choice <= len(phone_files):
                break
            else:
                print("Invalid choice. Please enter a number between 1 and", len(phone_files))
        except ValueError:
            print("Invalid input. Please enter a number.")

    selected_phone_file = phone_files[choice - 1]

    with open(os.path.join(phone_dir, selected_phone_file), "r") as f:
        apps_to_delete = []
        for line in f:
            line = line.strip()
            if not line.startswith("#"):  # Skip comment lines
                apps_to_delete.append(line)

    with open(os.path.join(phone_dir, selected_phone_file), "r") as f:
        apps_to_delete = []
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):  # Skip empty lines and comments
                apps_to_delete.append(line)

    
    phone_model = selected_phone_file[:-4]  # Remove the .txt extension
    print(f"\nApps to be deleted from {phone_model}:")

    for app in apps_to_delete:
        print(f"- {app}")

    while True:
        confirm = input("\nDo you want to proceed with the deletion? (y/N): ").lower()
        print("")
        if confirm in ['y', 'yes']:
            break
        elif confirm in ['n', 'no', '']:
            print("Deletion canceled.")
            return
        else:
            print("Invalid input. Please enter 'Y' or 'n'.")

    # Execute the ADB commands to delete the apps with error handling
    for app in apps_to_delete:
        result = subprocess.run(["adb", "shell", "pm", "uninstall", app], capture_output=True)
        if result.returncode != 0:
            print(f"Error deleting {app}: {result.stdout.decode('utf-8')}")
        else:
            print(f"Successfully deleted {app}")

    print("\nWhoosh, Done!")

if __name__ == "__main__":
    list_phones_and_apps()