- Use `logging`

  According to: https://ecederstrand.github.io/exchangelib/#troubleshooting

- Use `primary_smtp_address=...` param only for `Account` init

  Error. Attempt to add `autodiscover=True` param.

- Add `autodiscover=True` param

  Error. According
  to: https://learn.microsoft.com/en-us/exchange/client-developer/exchange-web-services/how-to-generate-a-list-of-autodiscover-endpoints

  Precisely step 2. and:

  `Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1018)'))`

- Use custom TLS validation

  According
  to: https://ecederstrand.github.io/exchangelib/#proxies-and-custom-tls-validation

  How to obtain a certificate? Visit url from step 2. in browser e.g. `Edge`.
  Click padlock at url start and export certificate to `.crt` or `.pem` file.

  Log: `DEBUG:exchangelib.transport:Auth type is NTLM`

  Error: `Auth type 'NTLM' requires credentials`

- Add `credentials=Credentials(...)` param

  Note: empty strings work for username and password.
