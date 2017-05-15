from django.contrib import admin
from certification.models import Student, Validator, Block
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from rsa import *
import base64
from blockchain import conf
from django.contrib import messages
from django.db import connection
connection.text_factory = str
class StudentAdmin(admin.ModelAdmin):
    fields = ['user']
    list_display = ['user','private_key','public_key']

    def save_model(self, request, obj, form, change):
        obj.private_key, obj.public_key = newkeys(2048)
        super(StudentAdmin, self).save_model(request, obj, form, change)


class ValidatorAdmin(admin.ModelAdmin):
    list_display = ['name','chain_length','get_blocks']
    def get_blocks(self, obj):
        return " ".join([str(p.id) for p in obj.blocks.all()])


class BlockAdmin(admin.ModelAdmin):
    fields = ['name','description','file']
    list_display  = ['id','block_number','student','nonce','validators','file','file_hash','previous_hash','hash','signature1','signature2']
    def save_model(self, request, obj, form, change):
        if change:
            messages.add_message(request, messages.INFO, "Cannot update changes. Ignore below message.")
            return False

        file = request.FILES['file']
        hash = SHA256.new()
        if file.multiple_chunks():
            for chunk in file.chunks():
              hash.update(chunk)
        else:    
              hash.update(file.read())
        file_hash = hash.digest()
        obj.file_hash = base64.b64encode(file_hash)

        for validator in Validator.objects.all():
            obj.pk = None
            obj.student = request.user.student
            pvt_key = request.user.student.private_key
            key = importKey(request.user.student.private_key)
            university_key = importKey(conf.PRIVATE_KEY)
            obj.signature1 = base64.b64encode(sign(file_hash,key))
            obj.signature2 = base64.b64encode(sign(file_hash,university_key))
            obj.validators = validator;
            last_block_number = validator.chain_length
            obj.block_number = last_block_number + 1

            previous_block =  Block.objects.filter(block_number=last_block_number,validators=validator)
            print previous_block
            if len(previous_block)==0:
                previous_hash = '0000000000000000000000000000000000000000000000000000000000000000'
            else:
                previous_hash = previous_block[0].hash    
            obj.previous_hash = previous_hash
            
            nonce = 0
            while(True):
                hash = check(obj.block_number,nonce,obj.name, obj.description,obj.file_hash,obj.signature1,obj.signature2,previous_hash)
                if(hash):
                    break
                print nonce    
                nonce = nonce + 1
    
            obj.nonce = nonce    
            obj.hash = hash
            obj.save()
            validator.chain_length=obj.block_number
            validator.blocks.add(obj)
            validator.save()
        return None


        

def check(block_number,nonce,hash,name, description,signature1,signature2,previous_hash):
    data = str(block_number)+str(nonce)+str(hash)+name+description+str(signature1)+str(signature2)+str(nonce)+str(previous_hash)
    f_hash= SHA256.new(data).hexdigest()
    if f_hash[0:3]=='000' :
        return f_hash
    else:  
        return False
admin.site.register(Student, StudentAdmin)
admin.site.register(Validator, ValidatorAdmin)
admin.site.register(Block, BlockAdmin)
