from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models


app = FastAPI()


models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "API Working"}


# STUDENT APIs
@app.post("/students/")
def create_student(name: str, email: str, course: str, db: Session = Depends(get_db)):
    student = models.Student(name=name, email=email, course=course)
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


@app.get("/students/")
def get_students(db: Session = Depends(get_db)):
    return db.query(models.Student).all()




@app.post("/courses/")
def create_course(name: str, fee: int, db: Session = Depends(get_db)):
    course = models.Course(name=name, fee=fee)
    db.add(course)
    db.commit()
    db.refresh(course)
    return course


@app.get("/courses/")
def get_courses(db: Session = Depends(get_db)):
    return db.query(models.Course).all()


@app.post("/invoices/")
def create_invoice(student_id: int, course_id: int, db: Session = Depends(get_db)):
    
    # Get course details
    course = db.query(models.Course).filter(models.Course.id == course_id).first()

    if not course:
        return {"error": "Course not found"}

    # Create invoice
    invoice = models.Invoice(
        student_id=student_id,
        course_id=course_id,
        amount=course.fee,   # 💰 auto fee
        status="pending"
    )

    db.add(invoice)
    db.commit()
    db.refresh(invoice)

    return invoice


@app.get("/invoices/")
def get_invoices(db: Session = Depends(get_db)):
    return db.query(models.Invoice).all()


@app.put("/invoices/{invoice_id}")
def pay_invoice(invoice_id: int, db: Session = Depends(get_db)):

    invoice = db.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()

    if not invoice:
        return {"error": "Invoice not found"}

    # Mark as paid
    invoice.status = "paid"

    db.commit()

    return {"message": "Payment successful"}