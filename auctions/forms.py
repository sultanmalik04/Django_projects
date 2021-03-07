from django import forms

class createListing(forms.Form):
    categries = [
        ('Home & Kitchen', 'Home & Kitchen'),
        ('Electronics', 'Electronics'),
        ('Books', 'Books'),
        ('Toys', 'Toys'),
        ('Fashion', 'Fashion'),
        ('Antiques', 'Antiques'),
        ('Automobile', 'Automobile')
    ]
    title = forms.CharField(max_length=50)
    description = forms.CharField(max_length=300, widget=forms.Textarea)
    base_price = forms.IntegerField()
    image_url = forms.URLField(max_length=500)
    category = forms.ChoiceField(choices=categries)
