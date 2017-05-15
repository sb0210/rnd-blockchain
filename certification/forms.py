from django import forms

class CertificateForm(forms.form):
	block_number = forms.IntegerField(label="Block Number")
	nonce = forms.IntegerField(label="Nonce")
	file = forms.FileField(label="Choose Cetificate file")
	
