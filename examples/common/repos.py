ALL_REPOS = {
    'sendgrid': [
        'sendgrid-csharp',
        'sendgrid-go',
        'sendgrid-java',
        'sendgrid-nodejs',
        'sendgrid-php',
        'sendgrid-python',
        'sendgrid-ruby',
        'smtpapi-csharp',
        'smtpapi-go',
        'smtpapi-java',
        'smtpapi-nodejs',
        'smtpapi-php',
        'smtpapi-python',
        'smtpapi-ruby',
        'csharp-http-client',
        'rest',
        'java-http-client',
        'php-http-client',
        'python-http-client',
        'ruby-http-client',
        'sendgrid-oai',
    ],
    'twilio': [
        'twilio-csharp',
        'twilio-java',
        'twilio-node',
        'twilio-php',
        'twilio-python',
        'twilio-ruby',
        'twilio-cli',
        'twilio-cli-core',
        'twilio-oai',
        'plugin-debugger',
        'homebrew-brew',
        'twilio-go',
        'twilio-oai-generator',
        'terraform-provider-twilio'
    ]
}

ALL_REPOS_CONSOLIDATED = ALL_REPOS['twilio'] + ALL_REPOS['sendgrid']
