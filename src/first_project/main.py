#!/usr/bin/env python
from random import randint
from pydantic import BaseModel
from crewai.flow.flow import Flow, listen, start
from .crews.poem_crew.poem_crew import createPoemCrew


class PoemState(BaseModel):
    poem_topic: str = ""
    sentence_count: int = 2
    poem: str = ""


class PoemFlow(Flow[PoemState]):

    @start()
    def get_poem_topic(self):
        """Starts the flow by asking for a poem topic."""
        response = input("Enter a topic for the poem: ")
        self.state.poem_topic = response  
        print("Poem topic set to", response)

    @listen(get_poem_topic)
    def generate_sentence_count(self):
        """Generates a random sentence count for the poem."""
        print("Generating sentence count")
        self.state.sentence_count = randint(1, 5)  

    @listen(generate_sentence_count)
    def generate_poem(self):
        """Generates a poem based on the topic and sentence count."""
        print("Generating poem")

        if not self.state.poem_topic:
            raise ValueError("Poem topic is missing!")

        result = createPoemCrew().kickoff(inputs={
            "poem_topic": self.state.poem_topic,
            "sentence_count": self.state.sentence_count
        })

        self.state.poem = result.raw  
        print("Poem generated:", self.state.poem)

    @listen(generate_poem)
    def save_poem(self):
        """Saves the generated poem to a file."""
        print("Saving poem...")
        with open("poem.txt", "w") as f:
            f.write(self.state.poem)
        print("Poem saved!")


def kickoff():
    """Starts the flow."""
    poem_flow = PoemFlow()
    poem_flow.kickoff()


def plot():
    """Plots the flow structure (if needed)."""
    poem_flow = PoemFlow()
    poem_flow.plot()


if __name__ == "__main__":
    kickoff()
