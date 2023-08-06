from __future__ import annotations

from datetime import date
from enum import IntEnum
from typing import Optional

from sqlalchemy import (
    CheckConstraint,
    Column,
    Date,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    column,
)
from sqlalchemy.orm import relationship

from valens.database import Base

# Alembic's autogenerate does not support CHECK constraints
# (https://github.com/sqlalchemy/alembic/issues/508). CHECK constraints get lost when running
# "batch" migrations for SQLite and must be stated explicitly in the migration script
# (https://alembic.sqlalchemy.org/en/latest/batch.html#including-check-constraints).
# CHECK constraints are only specified at the table level to enable the schema to be kept identical
# when applying migrations despite the aforementioned limitations.


class Sex(IntEnum):
    FEMALE = 0
    MALE = 1


class User(Base):
    __tablename__ = "user"

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String, unique=True, nullable=False)
    sex: Sex = Column(Enum(Sex), nullable=False)

    body_weight: list[BodyWeight] = relationship(
        "BodyWeight", backref="user", cascade="all, delete-orphan", passive_deletes=True
    )
    body_fat: list[BodyFat] = relationship(
        "BodyFat", backref="user", cascade="all, delete-orphan", passive_deletes=True
    )
    period: list[Period] = relationship(
        "Period", backref="user", cascade="all, delete-orphan", passive_deletes=True
    )
    exercises: list[Exercise] = relationship(
        "Exercise", backref="user", cascade="all, delete-orphan", passive_deletes=True
    )
    routines: list[Routine] = relationship(
        "Routine", backref="user", cascade="all, delete-orphan", passive_deletes=True
    )
    workouts: list[Workout] = relationship(
        "Workout", backref="user", cascade="all, delete-orphan", passive_deletes=True
    )


class BodyWeight(Base):
    __tablename__ = "body_weight"
    __table_args__ = (CheckConstraint(column("weight") > 0, name="weight_gt_0"),)

    user_id: int = Column(ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)
    date: date = Column(Date, primary_key=True)
    weight: float = Column(Float, nullable=False)


class BodyFat(Base):
    __tablename__ = "body_fat"
    __table_args__ = (
        CheckConstraint(column("chest") > 0, name="chest_gt_0"),
        CheckConstraint(column("abdominal") > 0, name="abdominal_gt_0"),
        CheckConstraint(column("tigh") > 0, name="tigh_gt_0"),
        CheckConstraint(column("tricep") > 0, name="tricep_gt_0"),
        CheckConstraint(column("subscapular") > 0, name="subscapular_gt_0"),
        CheckConstraint(column("suprailiac") > 0, name="suprailiac_gt_0"),
        CheckConstraint(column("midaxillary") > 0, name="midaxillary_gt_0"),
    )

    user_id: int = Column(ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)
    date: date = Column(Date, primary_key=True)
    chest: Optional[int] = Column(Integer)
    abdominal: Optional[int] = Column(Integer)
    tigh: Optional[int] = Column(Integer)
    tricep: Optional[int] = Column(Integer)
    subscapular: Optional[int] = Column(Integer)
    suprailiac: Optional[int] = Column(Integer)
    midaxillary: Optional[int] = Column(Integer)


class Period(Base):
    __tablename__ = "period"
    __table_args__ = (
        CheckConstraint(column("intensity") >= 1, name="intensity_ge_1"),
        CheckConstraint(column("intensity") <= 4, name="intensity_le_4"),
    )

    user_id: int = Column(ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)
    date: date = Column(Date, primary_key=True)
    intensity: int = Column(Integer, nullable=False)


class Exercise(Base):
    __tablename__ = "exercise"
    __table_args__ = (UniqueConstraint("user_id", "name"),)

    id: int = Column(Integer, primary_key=True)
    user_id: int = Column(ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    name: str = Column(String, nullable=False)

    sets: list[WorkoutSet] = relationship(
        "WorkoutSet", back_populates="exercise", cascade="all, delete-orphan"
    )
    routine_exercises: list[RoutineExercise] = relationship(
        "RoutineExercise", back_populates="exercise", cascade="all, delete-orphan"
    )


class Routine(Base):
    __tablename__ = "routine"
    __table_args__ = (UniqueConstraint("user_id", "name"),)

    id: int = Column(Integer, primary_key=True)
    user_id: int = Column(ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    name: str = Column(String, nullable=False)
    notes: str = Column(String)

    exercises: list[RoutineExercise] = relationship(
        "RoutineExercise", back_populates="routine", cascade="all, delete-orphan"
    )
    workouts: list[Workout] = relationship("Workout", back_populates="routine")


class RoutineExercise(Base):
    __tablename__ = "routine_exercise"
    __table_args__ = (
        CheckConstraint(column("position") > 0, name="position_gt_0"),
        CheckConstraint(column("sets") > 0, name="sets_gt_0"),
    )

    routine_id: int = Column(ForeignKey("routine.id", ondelete="CASCADE"), primary_key=True)
    position: int = Column(Integer, primary_key=True)
    exercise_id: int = Column(ForeignKey("exercise.id", ondelete="CASCADE"), nullable=False)
    sets: int = Column(Integer, nullable=False)

    routine: Routine = relationship("Routine", back_populates="exercises")
    exercise: Exercise = relationship("Exercise", back_populates="routine_exercises")


class Workout(Base):
    __tablename__ = "workout"

    id: int = Column(Integer, primary_key=True)
    user_id: int = Column(ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    routine_id: int = Column(ForeignKey("routine.id", ondelete="CASCADE"))
    date: date = Column(Date, nullable=False)
    notes: str = Column(String)

    routine: Routine = relationship("Routine", back_populates="workouts")
    sets: list[WorkoutSet] = relationship(
        "WorkoutSet", back_populates="workout", cascade="all, delete-orphan"
    )


class WorkoutSet(Base):
    __tablename__ = "workout_set"
    __table_args__ = (
        CheckConstraint(column("position") > 0, name="position_gt_0"),
        CheckConstraint(column("reps") > 0, name="reps_gt_0"),
        CheckConstraint(column("time") > 0, name="time_gt_0"),
        CheckConstraint(column("weight") > 0, name="weight_gt_0"),
        CheckConstraint(column("rpe") >= 0, name="rpe_ge_0"),
        CheckConstraint(column("rpe") <= 10, name="rpe_le_10"),
    )

    workout_id: int = Column(ForeignKey("workout.id", ondelete="CASCADE"), primary_key=True)
    position: int = Column(Integer, primary_key=True)
    exercise_id: int = Column(ForeignKey("exercise.id", ondelete="CASCADE"), nullable=False)
    reps: Optional[int] = Column(Integer)
    time: Optional[int] = Column(Integer)
    weight: Optional[float] = Column(Float)
    rpe: Optional[float] = Column(Float)

    workout: Workout = relationship("Workout", back_populates="sets")
    exercise: Exercise = relationship("Exercise", back_populates="sets")
