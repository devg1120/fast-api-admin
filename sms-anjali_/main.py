from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.status import HTTP_303_SEE_OTHER

app = FastAPI()

# 静的ファイル(CSS/JSなど)の設定（フォルダがある場合）
app.mount("/static", StaticFiles(directory="static"), name="static")

# テンプレートエンジンの設定
templates = Jinja2Templates(directory="templates")

# インメモリデータ
students = []
teachers = []
fees = []


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    total_students = len(students)
    total_teachers = len(teachers)
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "ts": total_students, "tt": total_teachers}
    )


@app.get("/new-student", response_class=HTMLResponse)
async def ns(request: Request):
    return templates.TemplateResponse("students/new.html", {"request": request})


@app.get("/new-teacher", response_class=HTMLResponse)
async def nt(request: Request):
    return templates.TemplateResponse("teachers/newt.html", {"request": request})


@app.get("/manage-students", response_class=HTMLResponse)
async def ms(request: Request):
    return templates.TemplateResponse(
        "students/manage.html",
        {"request": request, "students": students}
    )


@app.get("/manage-teachers", response_class=HTMLResponse)
async def mt(request: Request):
    return templates.TemplateResponse(
        "teachers/managet.html",
        {"request": request, "teachers": teachers}
    )


@app.post("/save-student")
async def ss(
    name: str = Form(...),
    age: str = Form(...),
    course: str = Form(...)
):
    if students:
        student_id = max([s['id'] for s in students]) + 1
    else:
        student_id = 1

    new_student = {
        'id': student_id,
        'name': name,
        'age': age,
        'course': course,
        'fees': 3000
    }
    students.append(new_student)
    # POST後のリダイレクトはステータスコード 303 (SEE OTHER) を指定します
    return RedirectResponse(url="/manage-students", status_code=HTTP_303_SEE_OTHER)


@app.post("/save-teacher")
async def st(
    name: str = Form(...),
    age: str = Form(...),
    subject: str = Form(...)
):
    if teachers:
        teacher_id = max([t['id'] for t in teachers]) + 1
    else:
        teacher_id = 1

    new_teacher = {
        'id': teacher_id,
        'name': name,
        'age': age,
        'subject': subject
    }
    teachers.append(new_teacher)
    return RedirectResponse(url="/manage-teachers", status_code=HTTP_303_SEE_OTHER)


@app.get("/delete-student/{id}")
async def ds(id: int):
    global students
    students = [s for s in students if s['id'] != id]
    return RedirectResponse(url="/manage-students", status_code=HTTP_303_SEE_OTHER)


@app.get("/delete-teacher/{id}")
async def dt(id: int):
    global teachers
    teachers = [t for t in teachers if t['id'] != id]
    return RedirectResponse(url="/manage-teachers", status_code=HTTP_303_SEE_OTHER)


@app.get("/print-student/{id}", response_class=HTMLResponse)
async def ps(request: Request, id: int):
    student = [s for s in students if s['id'] == id][0]
    return templates.TemplateResponse(
        'students/print.html',
        {"request": request, "student": student}
    )


@app.get("/print-teacher/{id}", response_class=HTMLResponse)
async def pt(request: Request, id: int):
    teacher = [t for t in teachers if t['id'] == id][0]
    return templates.TemplateResponse(
        'teachers/printt.html',
        {"request": request, "teacher": teacher}
    )


@app.get("/edit-student/{id}", response_class=HTMLResponse)
async def es(request: Request, id: int):
    student = [s for s in students if s['id'] == id][0]
    return templates.TemplateResponse(
        'students/edit.html',
        {"request": request, "student": student}
    )


@app.get("/edit-teacher/{id}", response_class=HTMLResponse)
async def et(request: Request, id: int):
    teacher = [t for t in teachers if t['id'] == id][0]
    return templates.TemplateResponse(
        'teachers/editt.html',
        {"request": request, "teacher": teacher}
    )


@app.post("/update-student")
async def us(
    id: int = Form(...),
    name: str = Form(...),
    age: str = Form(...),
    course: str = Form(...)
):
    student = [s for s in students if s['id'] == id][0]
    student['name'] = name
    student['age'] = age
    student['course'] = course
    return RedirectResponse(url="/manage-students", status_code=HTTP_303_SEE_OTHER)


@app.post("/update-teacher")
async def ut(
    id: int = Form(...),
    name: str = Form(...),
    age: str = Form(...),
    subject: str = Form(...)
):
    teacher = [t for t in teachers if t['id'] == id][0]
    teacher['name'] = name
    teacher['age'] = age
    teacher['subject'] = subject
    return RedirectResponse(url="/manage-teachers", status_code=HTTP_303_SEE_OTHER)


@app.get("/contact", response_class=HTMLResponse)
async def co(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})


@app.get("/new-fees", response_class=HTMLResponse)
async def nf(request: Request):
    return templates.TemplateResponse(
        "fees/new.html",
        {"request": request, "students": students}
    )


@app.post("/save-fees")
async def sf(
    s_id: int = Form(...),
    amount: str = Form(...)
):
    if fees:
        fees_id = max([f['id'] for f in fees]) + 1
    else:
        fees_id = 1

    new_fees = {
        'id': fees_id,
        's_id': s_id,
        'amount': amount
    }
    fees.append(new_fees)
    return RedirectResponse(url="/manage-fees", status_code=HTTP_303_SEE_OTHER)


@app.get("/manage-fees", response_class=HTMLResponse)
async def mf(request: Request):
    return templates.TemplateResponse(
        "fees/manage.html",
        {"request": request, "fees": fees, "students": students}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
