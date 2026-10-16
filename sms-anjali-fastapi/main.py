from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# 静的ファイルフォルダのマウント
app.mount("/static", StaticFiles(directory="static"), name="static")

# テンプレートの設定
templates = Jinja2Templates(directory="templates")


# 【解決策】古い環境でもHTML側の「url_for('static', filename='xxx')」を動かすためのカスタム関数
def custom_url_for(name: str, **path_params):
    # HTML内の 'filename' を FastAPI の仕様であるパスパラメータ（path）に変換する
    if name == 'static' and 'filename' in path_params:
        path_params['path'] = path_params.pop('filename')
    return app.url_path_for(name, **path_params)

# カスタム関数をJinja2のグローバル関数として上書き登録
templates.env.globals['url_for'] = custom_url_for


# メモリ内データベース
students = []
teachers = []
fees = []


def render(template_name: str, context: dict, request: Request) -> HTMLResponse:
    # テンプレート側で request オブジェクトを参照できるよう必ず文脈に追加
    context["request"] = request
    template = templates.env.get_template(template_name)
    html_content = template.render(context)
    return HTMLResponse(content=html_content, status_code=200)


@app.get('/')
def home(request: Request):
    total_students = len(students)
    total_teachers = len(teachers)
    return render(
        "index.html",
        {"ts": total_students, "tt": total_teachers},
        request=request
    )


@app.get('/new-student')
def ns(request: Request):
    return render("students/new.html", {}, request=request)


@app.get('/new-teacher')
def nt(request: Request):
    return render("teachers/newt.html", {}, request=request)


@app.get('/manage-students')
def ms(request: Request):
    return render("students/manage.html", {"students": students}, request=request)


@app.get('/manage-teachers')
def mt(request: Request):
    return render("teachers/managet.html", {"teachers": teachers}, request=request)


@app.post('/save-student')
def ss(
    name: str = Form(...),
    age: str = Form(...),
    course: str = Form(...)
):
    if students:
        id = max([s['id'] for s in students]) + 1
    else:
        id = 1

    new_student = {
        'id': id,
        'name': name,
        'age': age,
        'course': course,
        'fees': 3000
    }

    students.append(new_student)
    return RedirectResponse(url='/manage-students', status_code=303)


@app.post('/save-teacher')
def st(
    name: str = Form(...),
    age: str = Form(...),
    subject: str = Form(...)
):
    if teachers:
        id = max([t['id'] for t in teachers]) + 1
    else:
        id = 1

    new_teacher = {
        'id': id,
        'name': name,
        'age': age,
        'subject': subject
    }

    teachers.append(new_teacher)
    return RedirectResponse(url='/manage-teachers', status_code=303)


@app.get('/delete-student/{id}')
def ds(id: int):
    global students
    students = [s for s in students if s['id'] != id]
    return RedirectResponse(url='/manage-students', status_code=303)


@app.get('/delete-teacher/{id}')
def dt(id: int):
    global teachers
    teachers = [t for t in teachers if t['id'] != id]
    return RedirectResponse(url='/manage-teachers', status_code=303)


@app.get('/print-student/{id}')
def ps(request: Request, id: int):
    student_list = [s for s in students if s['id'] == id]
    student = student_list[0] if student_list else None
    return render('students/print.html', {"student": student}, request=request)


@app.get('/print-teacher/{id}')
def pt(request: Request, id: int):
    teacher_list = [t for t in teachers if t['id'] == id]
    teacher = teacher_list[0] if teacher_list else None
    return render('teachers/printt.html', {"teacher": teacher}, request=request)


@app.get('/edit-student/{id}')
def es(request: Request, id: int):
    student_list = [s for s in students if s['id'] == id]
    student = student_list[0] if student_list else None
    return render('students/edit.html', {"student": student}, request=request)


@app.get('/edit-teacher/{id}')
def et(request: Request, id: int):
    teacher_list = [t for t in teachers if t['id'] == id]
    teacher = teacher_list[0] if teacher_list else None
    return render('teachers/editt.html', {"teacher": teacher}, request=request)


@app.post('/update-student')
def us(
    id: int = Form(...),
    name: str = Form(...),
    age: str = Form(...),
    course: str = Form(...)
):
    student_list = [s for s in students if s['id'] == id]
    if student_list:
        student = student_list[0]
        student['name'] = name
        student['age'] = age
        student['course'] = course

    return RedirectResponse(url='/manage-students', status_code=303)


@app.post('/update-teacher')
def ut(
    id: int = Form(...),
    name: str = Form(...),
    age: str = Form(...),
    subject: str = Form(...)
):
    teacher_list = [t for t in teachers if t['id'] == id]
    if teacher_list:
        teacher = teacher_list[0]
        teacher['name'] = name
        teacher['age'] = age
        teacher['subject'] = subject

    return RedirectResponse(url='/manage-teachers', status_code=303)


@app.get('/contact')
def co(request: Request):
    return render("contact.html", {}, request=request)


@app.get('/new-fees')
def nf(request: Request):
    return render("fees/new.html", {"students": students}, request=request)


@app.post('/save-fees')
def sf(
    s_id: int = Form(...),
    amount: str = Form(...)
):
    if fees:
        id = max([f['id'] for f in fees]) + 1
    else:
        id = 1

    new_fees = {
        'id': id,
        's_id': s_id,
        'amount': amount
    }

    fees.append(new_fees)
    return RedirectResponse(url='/manage-fees', status_code=303)


@app.get('/manage-fees')
def mf(request: Request):
    return render("fees/manage.html", {"fees": fees, "students": students}, request=request)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
