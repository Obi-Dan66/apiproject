# from django.test import TestCase
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from .models import Todo


class TodoModelTest(TestCase):
    def setUp(self):
        self.todo = Todo.objects.create(title="Test Todo", completed=False)

    def test_todo_model(self):
        self.assertTrue(isinstance(self.todo, Todo))
        self.assertEqual(str(self.todo), self.todo.title)


class TodoViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.todo = Todo.objects.create(title="Test Todo", completed=False)

    def test_get_all_todos(self):
        response = self.client.get(reverse("todo-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_todo_with_valid_data(self):
        data = {"title": "New Todo", "completed": False}
        response = self.client.post(reverse("todo-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Todo.objects.count(), 2)

    def test_create_todo_with_invalid_data(self):
        data = {"title": "", "completed": False}
        response = self.client.post(reverse("todo-list"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_single_todo(self):
        response = self.client.get(reverse("todo-detail", args=[self.todo.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_todo_with_valid_data(self):
        data = {"title": "Updated Todo", "completed": True}
        response = self.client.put(reverse("todo-detail", args=[self.todo.id]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.todo.refresh_from_db()
        self.assertEqual(self.todo.title, "Updated Todo")
        self.assertEqual(self.todo.completed, True)

    def test_update_todo_with_invalid_data(self):
        data = {"title": "", "completed": True}
        response = self.client.put(reverse("todo-detail", args=[self.todo.id]), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_todo(self):
        response = self.client.delete(reverse("todo-detail", args=[self.todo.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Todo.objects.count(), 0)