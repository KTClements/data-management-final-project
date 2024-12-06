# Instructions for Configuring and Running the MDT Inventory Management Program

## Step 1: Update `app.py` for Directory Configuration

1. Open the `app.py` file located in the `backend` folder.

2. Locate the following directory paths in the file:
   - `file_path = 'C:\\Users\\KC\\Desktop\\data-management-final-project-main\\data\\MDT INVENTORY.xlsx'`
   - `csv_path = 'C:\\Users\\KC\\Desktop\\data-management-final-project-main\\data\\Returned_Report.csv'`

3. Change the paths to match your current directory structure. For example:
   - If the program is located in `D:\Projects\Data Management`, update the paths like this:

     file_path = 'D:\\Projects\\Data Management\\data\\MDT INVENTORY.xlsx'
     csv_path = 'D:\\Projects\\Data Management\\data\\Returned_Report.csv'

4. Save the changes to the `app.py` file.

---

## Step 2: Manually Booting the Program (If `.exe` Fails)

If the `.exe` file does not work, you can manually run the program by following these steps:

### Backend

1. Open a terminal or command prompt.
2. Navigate to the `backend` folder using the `cd` command:
 
   cd <path-to-backend-folder>
 
   Example:
 
   cd C:\Users\<YourName>\Desktop\Data Management - final project\backend

3. Install the required Python dependencies:

   pip install -r requirements.txt

4. Run the backend server:

   python app.py


### Frontend

1. Open a new terminal or command prompt.
2. Navigate to the `frontend` folder:

   cd <path-to-frontend-folder>

   Example:

   cd C:\Users\<YourName>\Desktop\Data Management - final project\frontend

3. Install the required Node.js dependencies:

   npm install

4. Start the React development server:

   npm start


---

## Step 3: Access the Application

1. Once both the backend and frontend servers are running, open your web browser.
2. Navigate to:

   http://localhost:3000

   This will load the MDT Inventory Management web application.

---

## Notes

1. Ensure you have Python and Node.js installed on your machine.
2. For issues with dependencies:
   - Run `pip install` for missing Python packages.
   - Run `npm install` for missing Node.js packages.
