from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from healthcenter.validators import validate_no_sql_injection   
# Create your models here.
class About(models.Model):
    """Information about the Public Health Center"""
    title = models.CharField(max_length=200)
    banner_title = models.CharField(max_length=200, blank=True, help_text="Banner title for homepage")
    banner_image_1 = models.ImageField(upload_to='banner_images/', blank=True, null=True)
    banner_image_2 = models.ImageField(upload_to='banner_images/', blank=True, null=True)
    banner_image_3 = models.ImageField(upload_to='banner_images/', blank=True, null=True)
    banner_description_1 = models.CharField(max_length=300, blank=True, help_text="Banner description 1")
    banner_description_2 = models.CharField(max_length=300, blank=True, help_text="Banner description 2")
    banner_description_3 = models.CharField(max_length=300, blank=True, help_text="Banner description 3")
    welcome_message = CKEditor5Field('Welcome Message', config_name='default', blank=True)
    short_description = CKEditor5Field('Short Description', config_name='default', blank=True)
    mission = CKEditor5Field('Mission', config_name='default')
    vision = CKEditor5Field('Vision', config_name='default')
    history = CKEditor5Field('History', config_name='default', blank=True)
    description = CKEditor5Field('Description', config_name='default')
    established_year = models.IntegerField(null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = CKEditor5Field('Address', config_name='default')
    working_hours = CKEditor5Field('Working Hours', config_name='default', help_text="e.g., Mon-Fri: 8:00 AM - 4:30 PM")
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False, help_text="Mark as active/published")

    class Meta:
        verbose_name = "About Us"
        verbose_name_plural = "About Us"

    def __str__(self):
        return self.title

class Content(models.Model):
    """Additional content for the Health Center"""
    heading = models.CharField(max_length=200)
    body = CKEditor5Field('Body', config_name='default', validators=[validate_no_sql_injection])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Content"
        verbose_name_plural = "Contents"

    def __str__(self):
        return self.heading
    
class Home(models.Model):
    """Home page content for the Health Center"""
    banner_title = models.CharField(max_length=200) 
    banner_image_1 = models.ImageField(upload_to='home/', blank=True, null=True)    
    banner_image_2 = models.ImageField(upload_to='home/', blank=True, null=True)    
    banner_image_3 = models.ImageField(upload_to='home/', blank=True, null=True)
    banner_description_1 = models.CharField(max_length=500, blank=True, null=True)
    banner_description_2 = models.CharField(max_length=500, blank=True, null=True)
    banner_description_3 = models.CharField(max_length=500, blank=True, null=True)
    welcome_message = CKEditor5Field('Welcome Message', config_name='default')
    short_description = CKEditor5Field('Short Description', config_name='default')
    vision = CKEditor5Field('Vision', config_name='default')
    mission = CKEditor5Field('Mission', config_name='default')
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='home/', blank=True, null=True)
    video_embed = models.TextField(blank=True, null=True, help_text="Paste embed code or video URL here")

    class Meta:
        verbose_name = "Home Page"
        verbose_name_plural = "Home Page"

    def __str__(self):
        return "Home Page Content"
    

class CategoryPortfolio(models.Model):
    """Categories for Portfolio entries"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Category Portfolio"
        verbose_name_plural = "Category Portfolios"

    def __str__(self):
        return self.name    
class Portfolio(models.Model):
    """Portfolio entries for the Health Center"""
    title = models.CharField(max_length=200)
    category = models.ForeignKey(CategoryPortfolio, on_delete=models.SET_NULL, blank=True, null=True)
    description = CKEditor5Field('Description', config_name='default')
    image = models.ImageField(upload_to='portfolio/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Portfolio"
        verbose_name_plural = "Portfolios"

    def __str__(self):
        return self.title