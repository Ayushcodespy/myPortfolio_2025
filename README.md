# My Portfolio 2025

This is a Django-based personal portfolio website with:

- portfolio home page
- projects listing page
- project detail page
- Django admin panel
- Razorpay payment flow for source code purchase
- email sending after successful payment
- fallback JSON data for projects, education, and certificates

---

## 1. Project Flow

### English

This project uses **two content sources**:

1. **Database content**
   - Managed from Django admin
   - Best for normal updates

2. **Fallback JSON content**
   - Used when database data is missing
   - Also useful when you want to manage data manually from files

The website now merges both:

- if a project exists in the database and JSON with the same `slug`, the **database version wins**
- if a project exists only in JSON, it will still show on the website
- same idea is used for education and certificates

So you do **not** need to keep editing `myApp/views.py`.

### Hinglish

Is project me content **2 jagah** se aa sakta hai:

1. **Database se**
   - Django admin panel se manage hota hai
   - Regular updates ke liye best

2. **JSON files se**
   - Jab DB me data na ho tab fallback ke liye
   - Ya jab manually file edit karna ho

Ab system dono ko merge karta hai:

- agar same `slug` wala project DB aur JSON dono me hai, to **DB wala show hoga**
- agar koi project sirf JSON me hai, to wo bhi site par show hoga

Matlab ab `views.py` me baar-baar changes karne ki zarurat nahi hai.

---

## 2. Important Files

### Main files

- `myApp/views.py`
  - page rendering
  - payment flow
  - email sending
  - JSON fallback loading

- `myApp/models.py`
  - database models for:
    - `Education`
    - `Certificate`
    - `Project`

- `myApp/fallback_data/projects.json`
  - manual fallback project data

- `myApp/fallback_data/education.json`
  - manual fallback education data

- `myApp/fallback_data/certificates.json`
  - manual fallback certificate data

- `templates/index.html`
  - homepage UI

- `templates/projects.html`
  - all projects page

- `templates/project_detail.html`
  - single project detail page

- `myPortfolio_2025/settings.py`
  - Django settings

- `.env`
  - secrets and environment variables

---

## 3. How Data Is Loaded

### English

For projects, education, and certificates:

1. Django first tries to load data from the database
2. Then fallback JSON data is loaded
3. Both are merged
4. Database items get priority if duplicates exist

### Hinglish

Flow simple hai:

1. Pehle DB se data aata hai
2. Phir JSON fallback load hota hai
3. Dono merge hote hain
4. Agar duplicate mila to DB wala data priority leta hai

---

## 4. How To Run Locally

### Windows PowerShell

```powershell
.\venv\Scripts\activate
python manage.py runserver
```

Open:

- `http://127.0.0.1:8000/`
- admin: `http://127.0.0.1:8000/admin/`

---

## 5. How To Add A New Project

You have **2 ways**.

### Option A: From Admin Panel

Use this if your deployment/storage supports uploads properly.

Steps:

1. Open `/admin`
2. Go to `Projects`
3. Click `Add Project`
4. Fill:
   - `slug`
   - `title`
   - `short_description`
   - `long_description`
   - `tech_stack`
   - `highlights`
   - `demo_url`
   - `source_code_price_inr`
   - `is_featured`
   - `order`

### Important for Vercel

On Vercel, file uploads to local disk do not work because filesystem is read-only.

So for deployed site, prefer:

- `image_path` for project image
- `source_code_url` for downloadable zip URL

### Option B: From JSON file

Edit:

- `myApp/fallback_data/projects.json`

Add a new object like this:

```json
{
  "slug": "my-new-project",
  "title": "My New Project",
  "short_description": "Short summary of the project.",
  "long_description": "Detailed project description here.",
  "tech_stack": ["Django", "HTML", "CSS", "JavaScript"],
  "highlights": ["Responsive UI", "Admin dashboard", "Fast performance"],
  "image_path": "images/projects/img/my-new-project.png",
  "demo_url": "https://example.com",
  "source_code_price_inr": 499,
  "source_code_zip": "source_code/zip_files/my-new-project.zip",
  "source_code_url": "/static/source_code/my-new-project.zip",
  "is_featured": true,
  "order": 7
}
```

### Hinglish

Agar new project add karna hai aur easy rakhna hai, to:

1. `myApp/fallback_data/projects.json` kholo
2. Same format ka ek naya project object add karo
3. `slug` unique rakho
4. `image_path` me image ka path ya URL do
5. `source_code_url` me zip file ka public link do
6. `is_featured: true` rakhoge to homepage par bhi show hoga

---

## 6. Project Field Meaning

- `slug`
  - unique id for project
  - example: `med-store-plus`

- `title`
  - project name shown on UI

- `short_description`
  - short text for project cards

- `long_description`
  - full description for project detail page

- `tech_stack`
  - list of technologies

- `highlights`
  - list of major project points

- `image_path`
  - image path or public image URL

- `demo_url`
  - live project link

- `source_code_price_inr`
  - price in INR

- `source_code_zip`
  - internal/source file path reference

- `source_code_url`
  - public URL for sending source code after payment

- `is_featured`
  - if `true`, project appears on homepage featured section

- `order`
  - controls display order

---

## 7. How To Add Education

### JSON method

Edit:

- `myApp/fallback_data/education.json`

Add a new item:

```json
{
  "title": "BCA",
  "institution": "Example University",
  "date_range": "2026 - 2029",
  "description": "Description here.",
  "order": 6
}
```

### Hinglish

Study/education add karne ke liye:

1. `myApp/fallback_data/education.json` kholo
2. Naya object add karo
3. `order` ka number decide karega kis sequence me show hoga

---

## 8. How To Add Certificate

### JSON method

Edit:

- `myApp/fallback_data/certificates.json`

Add a new item:

```json
{
  "title": "My Certificate",
  "issuer": "Issuer Name",
  "issued_date": "January 2026",
  "drive_link": "https://drive.google.com/your-link",
  "order": 8
}
```

### Hinglish

Certificate add karne ke liye:

1. `myApp/fallback_data/certificates.json` kholo
2. Naya certificate object add karo
3. `drive_link` me public link do
4. `order` se position control hogi

---

## 9. Why Admin Image Upload Fails On Vercel

### English

Vercel uses a read-only filesystem for deployed Django apps.
Because of that:

- uploading images to `media/`
- uploading zip files to `media/`

does not work in production on Vercel.

### Hinglish

Vercel par local file upload kaam nahi karta kyunki deployed server ka filesystem read-only hota hai.

Isliye:

- admin me image upload
- admin me zip upload

production me fail ho sakta hai.

### Best workaround

Use:

- `image_path` with public image URL
- `source_code_url` with public zip URL

Or integrate external storage later:

- Cloudinary
- Supabase Storage
- AWS S3

---

## 10. Payment Flow

### English

Current flow:

1. User opens a project detail page
2. User enters email
3. Razorpay order is created
4. User completes payment
5. Payment is verified
6. Email is sent to buyer
7. Admin notification is sent

### Hinglish

Payment flow ye hai:

1. User project detail page open karta hai
2. Apna email deta hai
3. Razorpay order banta hai
4. Payment complete hota hai
5. Payment verify hota hai
6. Buyer ko email jata hai
7. Aapko bhi notification milti hai

---

## 11. Environment Variables

These should stay in `.env` or Vercel Environment Variables.

Examples:

```env
SECRET_KEY=your-secret-key
DEBUG=false
ALLOWED_HOSTS=ayushcodespy.vercel.app
DATABASE_URL=your-database-url
RAZORPAY_KEY_ID=your-razorpay-key
RAZORPAY_KEY_SECRET=your-razorpay-secret
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=465
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_USE_SSL=true
EMAIL_USE_TLS=false
DEFAULT_FROM_EMAIL=your-email@gmail.com
PORTFOLIO_ADMIN_EMAIL=your-email@gmail.com
SITE_URL=https://ayushcodespy.vercel.app
EMAIL_LOGO_URL=https://ayushcodespy.vercel.app/static/images/ayush.png
```

---

## 12. If A Project Is Not Showing

Check these things:

1. `slug` is unique
2. JSON syntax is valid
3. comma placement in JSON is correct
4. image path is correct
5. project is either in DB or in fallback JSON
6. if DB has same slug, DB version may override JSON version
7. if homepage section is involved, check `is_featured`

### Especially for `med-store-plus`

Make sure the image path matches the real file name:

```text
images/projects/img/med-store-plus.png
```

---

## 13. Recommended Workflow For You

### Best practical setup

- use **admin** for text/content updates when possible
- use **fallback JSON** for quick manual updates
- use public image/zip URLs on deployed Vercel site

### My recommendation

For your current setup:

1. Keep admin for normal content
2. Keep JSON as backup/manual source
3. Use `image_path` and `source_code_url` instead of upload fields on Vercel

---

## 14. Future Improvements

Later, if needed, we can add:

- Cloudinary for image uploads
- Supabase Storage for zip files
- a custom dashboard to edit JSON from UI
- import/export sync between DB and JSON

---

## 15. Quick Summary

### If you want to add a project

Edit:

- `myApp/fallback_data/projects.json`

### If you want to add education

Edit:

- `myApp/fallback_data/education.json`

### If you want to add certificate

Edit:

- `myApp/fallback_data/certificates.json`

### If you want admin changes to show

- add/update from Django admin
- DB version gets priority

---

If you want, next I can also add:

1. a `sample_project.json` template
2. comments/examples in a separate docs file
3. a small script to validate JSON before you run the project
