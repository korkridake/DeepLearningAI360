# Structured LLM Output Course Announcement by DeepLearning.AI

Freeform LLM outputs are great for chat. But if you're building software? You need structure—something your system can reliably read and use.

In this new short course, Getting Structured LLM Output, built with @dottxtai, taught by @willkurt and @cameron_pfiffer, you’ll learn how to guide LLMs to produce structured outputs using:

✨ OpenAI’s structured output API
🔁 The Instructor library for output validation and re-prompting
🧩 DotTxt’s Outlines library for token-level control using regular expressions (regex) to enforce structure

One of the hands-on projects of the course is a social media analysis agent. It reads user posts, identifies sentiment, checks if a reply is needed, and, if there's an issue, automatically generates a support ticket. All output as clean, structured JSON that other tools can process.

[DeepLearning.AI on X: "Freeform LLM outputs are great for chat. But if you're building software? You need structure—something your system can reliably read and use. In this new short course, Getting Structured LLM Output, built with @dottxtai, taught by @willkurt and @cameron_pfiffer, you’ll learn how https://t.co/QoCteLAJyW" / X](https://x.com/DeepLearningAI/status/1907455569830494673)

## What you'll learn

- Get an overview of structured output generation, its importance, and the different approaches to generating them.
- Build a social media agent using structured output and learn how to use re-prompting libraries like instructor.
- Understand the concepts behind constrained decoding and how the LLM logits are modified to get a particular output structure.

## About this course

Welcome to Getting Structured LLM Output, built in partnership with DotTxt, and taught by Will Kurt, Founding Engineer, and Cameron Pfiffer, Developer Relations Engineer at DotTxt.

When building production-ready software, it’s challenging to parse through and rely on freeform text outputs. Structured outputs—like JSON—solve this by converting natural language into consistent, clear, and programmable data that a machine can read and process.

In this course, you’ll learn how to generate structured outputs while building several use cases, including a social media analysis agent.

You’ll gain a fundamental understanding of structured outputs and learn efficient ways to generate outputs in your defined schema or format. You’ll begin by using structured output APIs, then follow it up by utilizing re-prompting libraries like “instructor” to generate structured output. Afterward, you’ll learn how constrained decoding works, in which constraints are applied on each subsequent token generated, blocking any tokens that don’t fit your defined schema.

In detail, you’ll:

- Learn why structured outputs are important, how they allow for scalable software development, and the different approaches to generate them, including vendor-provided APIs, re-prompting libraries, and structured generation.
- Build a simple social media agent using OpenAI’s structured output API, learn how to define a model’s desired structured output using Pydantic, and perform basic programming with your outputs, such as importing structured data into a data frame using pandas.
- Learn how to use the open-source library “instructor,” which checks the structured output of the model and re-prompts the model until it validates the desired output, and explore the limitations of this approach.
- Understand how structured generation by “outlines” works by modifying LLM logits, per token generated based on instruction, to give a particular output structure.
- Learn how regular expressions, which power outlines, are represented as finite-state machine, and how they can be used to develop a range of structured output beyond JSON.
- By the end of this course, you’ll have broadened your knowledge of the approaches you can use to get structured outputs from your LLM applications.

## Who should join?
It’s helpful to be familiar with Python, the basics of LLM prompting, and LLM application development.