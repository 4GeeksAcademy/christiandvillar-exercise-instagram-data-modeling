from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum, Column, Integer, String, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship, declarative_base
from eralchemy2 import render_er
from datetime import datetime
import enum

# Configuración de SQLAlchemy
db = SQLAlchemy()
Base = declarative_base()

# Enum para tipo de notificación
class NotificationTypeEnum(enum.Enum):
    follow = "follow"
    like = "like"
    comment = "comment"

# Definición de modelos
class User(Base):
    __tablename__ = 'user'
    UserId = Column(Integer, primary_key=True)
    username = Column(String(30), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(20), nullable=False)
    firstName = Column(String(20))
    lastName = Column(String(20))
    bio = Column(String(150))
    profileImage = Column(String(250))
    createdAt = Column(Date, nullable=False, default=datetime.utcnow)

class Post(Base):
    __tablename__ = 'post'
    PostId = Column(Integer, primary_key=True)
    UserId = Column(Integer, ForeignKey('user.UserId'), nullable=False)
    imageUrl = Column(String(250), nullable=False)
    caption = Column(String(150))
    createdAt = Column(Date, nullable=False, default=datetime.utcnow)
    user = relationship("User", backref="posts")

class Like(Base):
    __tablename__ = 'like'
    LikeId = Column(Integer, primary_key=True)
    UserId = Column(Integer, ForeignKey('user.UserId'), nullable=False)
    PostId = Column(Integer, ForeignKey('post.PostId'), nullable=False)
    createdAt = Column(Date, nullable=False, default=datetime.utcnow)
    user = relationship("User", backref="likes")
    post = relationship("Post", backref="likes")

class Comment(Base):
    __tablename__ = 'comment'
    CommentId = Column(Integer, primary_key=True)
    UserId = Column(Integer, ForeignKey('user.UserId'), nullable=False)
    PostId = Column(Integer, ForeignKey('post.PostId'), nullable=False)
    content = Column(String(250), nullable=False)
    createdAt = Column(Date, nullable=False, default=datetime.utcnow)
    user = relationship("User", backref="comments")
    post = relationship("Post", backref="comments")

class Follow(Base):
    __tablename__ = 'follow'
    FollowId = Column(Integer, primary_key=True)
    followerId = Column(Integer, ForeignKey('user.UserId'), nullable=False)
    followedId = Column(Integer, ForeignKey('user.UserId'), nullable=False)
    createdAt = Column(Date, nullable=False, default=datetime.utcnow)
    follower = relationship("User", foreign_keys=[followerId])
    followed = relationship("User", foreign_keys=[followedId])

class Notification(Base):
    __tablename__ = 'notification'
    NotificationId = Column(Integer, primary_key=True)
    UserId = Column(Integer, ForeignKey('user.UserId'), nullable=False)
    fromUserId = Column(Integer, ForeignKey('user.UserId'), nullable=False)
    type = Column(Enum(NotificationTypeEnum), nullable=False)
    PostId = Column(Integer, ForeignKey('post.PostId'), nullable=True)
    createdAt = Column(Date, nullable=False, default=datetime.utcnow)
    isRead = Column(Boolean, default=False)
    user = relationship("User", foreign_keys=[UserId])
    fromUser = relationship("User", foreign_keys=[fromUserId])
    post = relationship("Post", backref="notifications")

class SavedPost(Base):
    __tablename__ = 'saved_post'
    SavedPostId = Column(Integer, primary_key=True)
    UserId = Column(Integer, ForeignKey('user.UserId'), nullable=False)
    PostId = Column(Integer, ForeignKey('post.PostId'), nullable=False)
    createdAt = Column(Date, nullable=False, default=datetime.utcnow)
    user = relationship("User", backref="saved_posts")
    post = relationship("Post", backref="saved_by")

class Story(Base):
    __tablename__ = 'story'
    StoryId = Column(Integer, primary_key=True)
    UserId = Column(Integer, ForeignKey('user.UserId'), nullable=False)
    imageUrl = Column(String(250), nullable=False)
    caption = Column(String(150))
    createdAt = Column(Date, nullable=False, default=datetime.utcnow)
    expirationDate = Column(Date, nullable=False)
    user = relationship("User", backref="stories")

# Generar el diagrama
try:
    render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem generating the diagram")
    raise e
