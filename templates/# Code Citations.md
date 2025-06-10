# Code Citations

## License: unknown
https://github.com/rubenmqz/mypointDjango/tree/731a9226cd50480eef6e8402775bdd8c7d27068e/users/forms.py

```
"username", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.
```

