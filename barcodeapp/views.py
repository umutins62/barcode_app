import os
from django.core.files import File
from django.http import FileResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Barcode
import qrcode


def index(request):
    barcodes = Barcode.objects.all()
    return render(request, 'index.html', {'barcodes': barcodes})


def create_barcode(request):
    if request.method == 'POST':
        code = request.POST.get('code')

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

        qr.add_data(code)
        qr.make(fit=True)

        img = qr.make_image(fill='black', back_color='white')

        # Görüntüyü bir dosya olarak kaydet
        file_path = f"static/barcodes/{code}.png"
        img.save(file_path)

        # Görüntü dosyasını Django modeline kaydet
        barcode_instance = Barcode(code=code)
        barcode_instance.image.save(
            f"{code}.png",
            File(open(file_path, 'rb'))
        )
        barcode_instance.save()

        print(f"QR kod oluşturuldu ve '{file_path}' olarak kaydedildi.")
        return redirect('index')

    return render(request, 'create_barcode.html')


def delete_barcode(request, pk):
    barcode = Barcode.objects.get(pk=pk)
    barcode.delete()
    return redirect('index')


def save_barcode(request, pk):
    barcode_instance = get_object_or_404(Barcode, id=pk)  # Model ve primary key ile doğru bir şekilde sorgu yapılır
    img = barcode_instance.image  # Burada image_field, Barcode modelindeki ilgili ImageField'in adıdır.

    # Eğer ImageField'in adı image_field değilse, doğru adı buraya yazın
    file_path = img.path
    response = FileResponse(open(file_path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
    return response  # İndirme işlemi için response döndürülmeli, index sayfasına yönlendirme bu noktada mantıklı değil.