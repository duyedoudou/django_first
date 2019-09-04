from django.shortcuts import render
from django.http import FileResponse
from .forms import PdfExtractForm,PdfMergeForm,PdfReplaceForm
import os
import PyPDF2
import zipfile


def pdf_single_page_extract(request):
    if request.method ==  'POST':
        form = PdfExtractForm(request.POST,request.FILES)
        if form.is_valid():
            # 获取上传文件
            f = form.cleaned_data['file']
            # 转化为PDF对象
            pdfobj = PyPDF2.PdfFileReader(f)

            # 获取需提取的页面列表
            page_list = form.cleaned_data['page'].split(',')

            # 创建zip对象
            zf = zipfile.ZipFile(os.path.join('media/pdfs/ex_pdf','extracted_page.zip'),'w')

            for page_num in page_list:
                page_index = int(page_num)-1
                page_obj = pdfobj.getPage(page_index)
                # 创建新的PDFwrite
                pdf_write = PyPDF2.PdfFileWriter()
                # 添加文件
                pdf_write.addPage(page_obj)

                pdf_file_path = os.path.join('media/pdfs/ex_pdf','extract_page_{}.pdf'.format(page_num))

                with open(pdf_file_path,'wb') as pdfOutputFile:
                    pdf_write.write(pdfOutputFile)

                zf.write(pdf_file_path)
            zf.close()

            # 给用户返回压缩包
            # extractedPage = open(pdf_file_path, 'rb')
            extractedPage = open(os.path.join('media/pdfs/ex_pdf', 'extracted_page.zip'), 'rb')
            response = FileResponse(extractedPage)
            response['content_type'] = "application/zip"
            response['Content-Disposition'] = 'attachment; filename="extracted_pages.zip"'
            return response


    else:
        form = PdfExtractForm()

    return render(request, 'pdf/pdf_extract.html', {'form': form})

def pdf_range_page_extract(request):
    if request.method == 'POST':
        form = PdfExtractForm(request.POST,request.FILES)
        if form.is_valid():
            f = form.cleaned_data['file']
            pdfobj = PyPDF2.PdfFileReader(f)
            page_range = form.cleaned_data['page'].split('-')
            page_start = int(page_range[0])
            page_end = int(page_range[1])

            pdf_file_path = os.path.join('media/pdfs/range_pdf','extract_page_range{}-{}.pdf'.format(page_start,page_end))
            pdfOutputFile = open(pdf_file_path,'ab+')

            # 创建新的PDFwrite
            pdf_write = PyPDF2.PdfFileWriter()

            for page_num in range(page_start,page_end+1):
                page_index = int(page_num) - 1
                page_obj = pdfobj.getPage(page_index)
                pdf_write.addPage(page_obj)

            pdf_write.write(pdfOutputFile)
            pdfOutputFile.close()

            extractedPage = open(pdf_file_path,'rb')
            response = FileResponse(extractedPage)
            response['content_type'] = "application/octet-stream"
            response['Content-Disposition'] = 'attachment; filename="extracted_pages.pdf"'
            return response

    else:
        form = PdfExtractForm()

    return render(request, 'pdf/pdf_range_extract.html', {'form': form})


def pdf_merge(request):
    if request.method == 'POST':
        form = PdfMergeForm(request.POST,request.FILES)
        if form.is_valid():
            f1 = form.cleaned_data['file1']
            f2 = form.cleaned_data['file2']
            f3 = form.cleaned_data['file3']
            f4 = form.cleaned_data['file4']
            f5 = form.cleaned_data['file5']

            f_list = [f1,f2,f3,f4,f5]

            pdfMerge = PyPDF2.PdfFileMerger()

            for f in f_list:
                if f:
                    pdfObj = PyPDF2.PdfFileReader(f)
                    pdfMerge.append(pdfObj)

            with open(os.path.join('media/pdfs/merge_pdf', 'merged_file.pdf'), 'wb') as pdfOutputFile:
                pdfMerge.write(pdfOutputFile)

            response = FileResponse(open(os.path.join('media/pdfs/merge_pdf', 'merged_file.pdf'), 'rb'))
            response['content_type'] = "application/octet-stream"
            response['Content-Disposition'] = 'attachment; filename="merged_file.pdf"'

            return response

    else:
        form = PdfMergeForm()

    return render(request, 'pdf/pdf_merge.html', {'form': form})
