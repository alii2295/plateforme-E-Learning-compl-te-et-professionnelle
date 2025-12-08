print("populate_db.py chargé !")

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from courses.models import Category, Course, Lesson
from accounts.models import Profile


class Command(BaseCommand):
    help = 'Populate database with sample data'

    def handle(self, *args, **kwargs):
        # Créer un instructeur
        instructor, created = User.objects.get_or_create(
            username='instructor',
            defaults={
                'email': 'instructor@example.com',
                'first_name': 'Jean',
                'last_name': 'Dupont'
            }
        )
        if created:
            instructor.set_password('password123')
            instructor.save()
            Profile.objects.create(user=instructor, is_instructor=True)

        # Créer des catégories
        categories_data = [
            {'name': 'Programmation', 'icon': 'bi-code-slash'},
            {'name': 'Design', 'icon': 'bi-palette'},
            {'name': 'Marketing', 'icon': 'bi-megaphone'},
            {'name': 'Business', 'icon': 'bi-briefcase'},
        ]

        for cat_data in categories_data:
            Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'icon': cat_data['icon']}
            )

        # Créer des cours
        programming_cat = Category.objects.get(name='Programmation')

        courses_data = [
            {
                'title': 'Python pour Débutants',
                'description': 'Apprenez les bases de Python de A à Z',
                'category': programming_cat,
                'level': 'beginner',
                'duration_hours': 10,
            },
            {
                'title': 'Django Avancé',
                'description': 'Maîtrisez le framework Django',
                'category': programming_cat,
                'level': 'advanced',
                'duration_hours': 20,
            },
        ]

        for course_data in courses_data:
            course, created = Course.objects.get_or_create(
                title=course_data['title'],
                defaults={
                    **course_data,
                    'instructor': instructor,
                    'is_published': True
                }
            )

            if created:
                # Créer des leçons
                for i in range(1, 4):
                    Lesson.objects.create(
                        course=course,
                        title=f'Leçon {i}: Introduction',
                        content=f'Contenu de la leçon {i}',
                        order=i,
                        duration_minutes=30,
                        is_preview=(i == 1)
                    )

        self.stdout.write(self.style.SUCCESS('Base de données peuplée avec succès!'))