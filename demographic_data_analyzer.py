import pandas as pd

def calculate_demographic_data(print_data=True):
    # Завантажуємо дані з CSV файлу
    df = pd.read_csv('adult.data.csv')
    # 1. Кількість людей кожної раси
    race_count = df['race'].value_counts()

    # 2. Середній вік чоловіків
    average_age_men = round(df[df['sex'] == 'Male']['age'].mean(), 1)

    # 3. Відсоток людей з бакалавратом
    percentage_bachelors = round((df['education'] == 'Bachelors').mean() * 100, 1)

    # 4. Відсоток людей з "advanced education" (Bachelors, Masters, Doctorate) що заробляють >50K
    advanced_edu = df['education'].isin(['Bachelors', 'Masters', 'Doctorate'])
    higher_education_rich = round((df[advanced_edu & (df['salary'] == '>50K')].shape[0] /
                                   df[advanced_edu].shape[0]) * 100, 1)

    # 5. Відсоток людей без "advanced education" що заробляють >50K
    lower_education = ~advanced_edu
    lower_education_rich = round((df[lower_education & (df['salary'] == '>50K')].shape[0] /
                                  df[lower_education].shape[0]) * 100, 1)

    # 6. Мінімальна кількість годин роботи на тиждень
    min_work_hours = df['hours-per-week'].min()

    # 7. Відсоток людей, які працюють мінімум годин і заробляють >50K
    num_min_workers = df[df['hours-per-week'] == min_work_hours]
    rich_min_workers = round((num_min_workers[num_min_workers['salary'] == '>50K'].shape[0] /
                              num_min_workers.shape[0]) * 100, 1)

    # 8. Країна з найбільшим відсотком людей, що заробляють >50K
    country_counts = df.groupby('native-country')['salary'].value_counts(normalize=True).unstack()
    country_counts = country_counts.fillna(0)
    highest_earning_country = country_counts['>50K'].idxmax()
    highest_earning_country_percentage = round(country_counts['>50K'].max() * 100, 1)

    # 9. Найпопулярніша робота у тих, хто заробляє >50K в Індії
    top_IN_occupation = df[(df['native-country'] == 'India') & (df['salary'] == '>50K')]['occupation'] \
        .value_counts().idxmax()

    # Повертаємо результати
    results = {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_min_workers,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage': highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }
    
    if print_data:
        print("Number of each race:\n", race_count)
        print("Average age of men:", average_age_men)
        print("Percentage with Bachelors degrees:", percentage_bachelors)
        print("Percentage with higher education that earn >50K:", higher_education_rich)
        print("Percentage without higher education that earn >50K:", lower_education_rich)
        print("Min work time:", min_work_hours, "hours/week")
        print("Percentage of rich among those who work fewest hours:", rich_min_workers)
        print("Country with highest percentage of rich:", highest_earning_country)
        print("Highest percentage of rich people in country:", highest_earning_country_percentage)
        print("Top occupations in India:", top_IN_occupation)
    
    return results
