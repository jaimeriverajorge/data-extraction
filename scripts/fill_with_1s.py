# a python script to fill any empty spot in a csv file with 1s
import pandas as pd


def main():
    name = "sinus_training_all_points_shuffled"
    df = pd.read_csv(f'{name}.csv')
    df = df.fillna(1)
    print(df)

    df.to_csv(f'{name}_filled.csv', index=False)

    return 1


if __name__ == "__main__":
    main()
