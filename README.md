# Summer Camp Registration Tracking System - User Guide

Welcome to the **Regent University Summer Camp Registration System**! This guide will help you understand how to use the web application for registering participants, joining the waitlist, and canceling registrations.

---

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [How to Use](#how-to-use)
  - [Register for the Camp](#register-for-the-camp)
  - [Join the Waitlist](#join-the-waitlist)
  - [Cancel a Registration](#cancel-a-registration)
- [FAQs](#faqs)
- [Technical Information](#technical-information)

---

## Overview
This system allows families to register for Regent University's STEM Summer Camp. Once all spots are filled, new registrants will be added to a waitlist automatically. Email notifications are sent for confirmations and cancellations.

---

## Features
- Register participants for camp.
- Automatically manage available spots and the waitlist.
- Send email confirmations upon registration and waitlist entry.
- Cancel registrations using a unique Registration ID.
- Easy-to-use and mobile-friendly interface.

---

## How to Use

### Register for the Camp
1. Go to the home page: https://campregistration.onrender.com/
2. Check the number of **Spots Available**.
3. If spots are available, fill out the **Name** and **Email** fields under "Sign Up".
4. Click the **Register** button.
5. You will receive an email with your **Registration ID**.

### Join the Waitlist
1. If camp registration is full, a message will appear: **"Registration is full. Join the waitlist!"**
2. Fill out the **Name** and **Email** fields under the waitlist section.
3. Click **Join Waitlist**.
4. You will receive an email confirming your waitlist status.

### Cancel a Registration
1. Locate your **Registration ID** (provided in your email confirmation).
2. Go to the "Cancel Registration" section.
3. Enter your **Registration ID** into the input box.
4. Click the **Cancel** button.
5. You will receive a confirmation email once your registration is canceled.

---

## FAQs

**Q: What happens when a spot opens up?**  
A: The system will notify the next person on the waitlist via email.

**Q: Can I update my registration information?**  
A: Please cancel your current registration and re-register with updated information.

**Q: I lost my Registration ID. What should I do?**  
A: Please contact the camp administration for assistance.

---

## Technical Information
- Built with **Python Flask** for backend.
- Uses **SQLite** database (`summer_camp.db`).
- Email functionality powered by **SMTP** through Gmail.
- Hosted via local server or deployable using **Gunicorn** for production.

---

Thank you for using the Summer Camp Registration System! We look forward to seeing you at camp!
