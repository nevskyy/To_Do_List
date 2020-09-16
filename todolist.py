from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def print_today_tasks():
    print()
    today = datetime.today()
    rows = session.query(Table).filter(Table.deadline == today.date()).all()
    print("Today", today.day, today.strftime('%b:'))
    if len(rows) == 0:
        print("Nothing to do!")
    else:
        count = 1
        for row in rows:
            print(f"{count}. {row}")
            count += 1
    print()
    session.commit()
    session.close()


def print_weeks_tasks():
    print()
    date_basket = []
    for task in session.query(Table).order_by(Table.deadline):
        one_date = task.deadline
        date_basket.append(one_date)

    today = datetime.today().date()
    week = []
    for i in range(7):
        day = today + timedelta(days=i)
        week.append(day)

    for day in week:
        print(f"{day.strftime('%A %d %b')}:")
        rows = session.query(Table).filter(Table.deadline == day).all()
        if day not in date_basket:
            print("Nothing to do!")
            print()
        else:
            count = 1
            for row in rows:
                print(f"{count}.{row}")
                count += 1
            print()
    session.commit()
    session.close()


def print_all_tasks():
    print("All tasks:")
    count = 1
    rows = session.query(Table).order_by(Table.deadline).all()
    for row in rows:
        print(f"{count}. {row.task}. {row.deadline.strftime('%#d %b')}")
        count += 1
    if count == 1:
        print("Nothing to do!")
    print()
    session.commit()
    session.close()


def print_missed_tasks():
    print()
    today = datetime.today().date()
    rows = session.query(Table).filter(Table.deadline < today).all()

    if not Table.deadline:
        print("Nothing is missed!")
    else:
        print("Missed tasks:")
        count = 1
        for row in rows:
            print(f"{count}. {row.task}. {row.deadline.strftime('%d %b')}")
            count += 1
    session.commit()
    session.close()


def add_task():
    new_row = Table(task=input('Enter task\n> '), deadline=datetime.strptime(input('Enter deadline\n> '), '%Y-%m-%d'))
    session.add(new_row)
    session.commit()
    session.close()
    print("The task has been added!\n")


def delete_tasks():
    print()
    # today = datetime.today().date()
    rows = session.query(Table).order_by(Table.deadline).all()
    print("Choose the number of the task you want to delete:")
    count = 1
    for row in rows:
        print(f"{count}. {row.task}. {row.deadline.strftime('%d %b')}")
        count += 1
    print()
    print(rows)
    # num_task = input('> ')
    session.delete(rows[int(input('> ')) - 1])
    print("The task has been deleted!")

    session.commit()
    session.close()


def menu():
    print("""1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit
""")


while True:
    menu()
    choice = input('> ')
    if choice == '1':
        print_today_tasks()
    elif choice == '2':
        print_weeks_tasks()
    elif choice == '3':
        print_all_tasks()
    elif choice == '4':
        print_missed_tasks()
    elif choice == '5':
        add_task()
    elif choice == '6':
        delete_tasks()
    elif choice == '0':
        print('\nBye!')
        break