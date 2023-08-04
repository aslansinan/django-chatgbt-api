from django.contrib import messages
from django.shortcuts import render, redirect
import openai
from  .models import Past
from django.core.paginator import Paginator
def home(request):
    # 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 ewa
    details = "home.html"
    if request.method == "POST":
        question = request.POST['question']
        past_responses = request.POST['past_responses']
        # set api key
        openai.api_key = "sk-ab72hPhuYcEVUEobStioT3BlbkFJsfJEKN3AB9ePI5LHOjMxewa"
        openai.Model.list()
        try:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=question,
                temperature=0,
                max_tokens=60,
                top_p=1.0,
                frequency_penalty=0.0
            )
            # parse response
            response = (response['choices'][0]["text"]).strip()

            # past_responses
            if "44sinan4434" in past_responses:
                past_responses = response
            else:
                past_responses = f"{past_responses}<br/><br/>{response}"
            record = Past(question=question,answer=response)
            record.save()

            return render(request, details, {"question": question, "response": response, "past_responses": past_responses})
        except Exception as e:
            return render(request, 'home.html',{"question": question, "response": e, "past_responses": past_responses})
    return render(request, details, {})

def past(request):
    details = "past.html"
    p = Paginator(Past.objects.all(), 3)
    page = request.GET.get('page')
    pages = p.get_page(page)
    nums = "a" * pages.paginator.num_pages
    past = Past.objects.all()
    return render(request, details, {"past": past, "pages": pages, "nums": nums})

def delete_past(request,Past_id):
    past = Past.objects.get(pk=Past_id)
    past.delete()
    messages.success(request, ("soru ve cevap silindi"))
    return redirect('past')