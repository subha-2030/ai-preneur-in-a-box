# Google Cloud Console OAuth 2.0 Configuration Guide

This document provides comprehensive instructions for configuring Google Cloud Console OAuth 2.0 to ensure compliance with Google's policies and prevent common authorization errors such as "Access blocked: Authorization Error".

## 1. Google Cloud Console OAuth Client Configuration

Follow these steps to create and configure an OAuth 2.0 Client ID for your application.

### Step-by-Step Setup Instructions

1.  **Navigate to the Credentials Page:**

    - Open the [Google Cloud Console](https://console.cloud.google.com/).
    - From the navigation menu, go to **APIs & Services > Credentials**.

2.  **Create OAuth Client ID:**

    - Click on **+ CREATE CREDENTIALS** and select **OAuth client ID**.

3.  **Configure the Client ID:**

    - **Application type:** Select **Web application**.
    - **Name:** Enter a descriptive name for your client ID (e.g., "AI-Preneur Web App").

4.  **Add Authorized Redirect URI:**

    - Under **Authorized redirect URIs**, click **+ ADD URI**.
    - Enter the following exact URI for local development:
      ```
      http://localhost:8000/api/v1/integrations/google/callback
      ```
    - **Important:** This URI must exactly match the one specified in your application's code.

5.  **Create the Client ID:**
    - Click the **CREATE** button.
    - A dialog will appear with your **Client ID** and **Client Secret**. Copy these values and store them securely in your application's environment variables.

### Required OAuth Scopes

The following scope is required for accessing Google Calendar data:

- `https://www.googleapis.com/auth/calendar.readonly`

This scope must be included in your application's authorization request.

## 2. OAuth Consent Screen Configuration

The consent screen informs users which permissions your application is requesting.

### Step-by-Step Setup Instructions

1.  **Navigate to the OAuth Consent Screen Page:**

    - In the Google Cloud Console, go to **APIs & Services > OAuth consent screen**.

2.  **User Type:**

    - For development, you can select **Internal**. This restricts access to users within your Google Workspace organization.
    - For production, you must select **External** to allow any Google user to access your application. This will require Google verification.

3.  **Application Information:**

    - **App name:** The name of your application (e.g., "AI-Preneur").
    - **User support email:** Your support email address.
    - **App logo:** (Optional but recommended) Upload your application's logo.

4.  **Authorized Domains:**

    - Click **+ ADD DOMAIN** and add your application's domain (e.g., `yourdomain.com`) for production. For local development, this is not required.

5.  **Developer Contact Information:**

    - Enter your email address for Google to contact you about your project.

6.  **Add Scopes:**

    - Click **SAVE AND CONTINUE**.
    - On the "Scopes" page, click **+ ADD OR REMOVE SCOPES**.
    - Find and select the `https://www.googleapis.com/auth/calendar.readonly` scope.
    - Click **UPDATE**.

7.  **Test Users (for External apps in testing mode):**

    - Click **SAVE AND CONTINUE**.
    - On the "Test users" page, click **+ ADD USERS** and add the Google accounts you will use for testing.

8.  **Review and Save:**
    - Review the summary and click **BACK TO DASHBOARD**.

## 3. Production Deployment Considerations

When deploying your application to production, you must update your OAuth configuration.

### Updating Redirect URIs

- You must add a new **Authorized redirect URI** for your production domain.
- Navigate to your OAuth 2.0 Client ID settings (**APIs & Services > Credentials**).
- Add the production redirect URI, for example:
  ```
  https://yourdomain.com/api/v1/integrations/google/callback
  ```

### SSL/HTTPS Requirements

- Google requires that all production redirect URIs use **HTTPS**. Your production server must have a valid SSL certificate. `localhost` is an exception.

### Domain Verification

- For external-facing applications, you must verify ownership of your authorized domains in Google Search Console.

## 4. Verification Checklist

Use this checklist to ensure your configuration is correct.

- [ ] **Application Type:** Is it set to "Web application"?
- [ ] **Redirect URI:** Does the URI in the Google Cloud Console exactly match the one in your application code (`http://localhost:8000/api/v1/integrations/google/callback` for local development)?
- [ ] **Scopes:** Is the `https://www.googleapis.com/auth/calendar.readonly` scope added to the consent screen and requested by your application?
- [ ] **Consent Screen Status:** Is the consent screen published? If it's in "testing" mode, are your test users added?
- [ ] **Client Credentials:** Are the correct Client ID and Client Secret used in your application's configuration?

### Common Misconfigurations

- **`redirect_uri_mismatch`:** The redirect URI in the request does not match any of the authorized redirect URIs in the Google Cloud Console.
- **`invalid_scope`:** The requested scope is invalid or not added to the consent screen.
- **`invalid_client`:** The Client ID or Client Secret is incorrect.

## 5. Troubleshooting Guide

### Common Error Messages

- **"Access blocked: Authorization Error" / "Error 400: invalid_request"**:

  - **Solution:** This is often a `redirect_uri_mismatch`. Double-check that the redirect URI in your Google Cloud Console project exactly matches the one your application is sending. Ensure there are no trailing slashes or typos.

- **"Error 403: access_denied"**:

  - **Solution:** The user has denied the permission request. Your application should handle this gracefully.

- **"Error 401: invalid_client"**:
  - **Solution:** Your Client ID or Client Secret is incorrect. Verify them from the Credentials page.

### How to Test the OAuth Flow

1.  Start your local application server.
2.  Access the endpoint that initiates the Google OAuth flow.
3.  You will be redirected to the Google consent screen.
4.  Log in with a test user account.
5.  Grant the requested permissions.
6.  You should be redirected back to your application's callback URL (`http://localhost:8000/api/v1/integrations/google/callback`).
7.  Your application should successfully exchange the authorization code for an access token.
