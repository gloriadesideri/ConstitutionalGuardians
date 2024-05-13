from PromptGenerator import PromptGenerator

if __name__ == "__main__":
    situations_file = "./Principle_c/principle_c_dataset.csv"
    prompt_generator = PromptGenerator(situations_file)
    #prompt_generator.generate_situations()
    prompt_generator.generate_final("./Principle_C/principle_c_dataset.csv_with_few_shots.csv")