# Reflection Log: Assignment 2 - Multi-Agent Travel Planning

Implementing this multi-agent workflow revealed the fundamental tension between autonomy and coordination in distributed systems. The Planner operates in isolation from real-time data, relying entirely on its training corpus to generate itineraries. This constraint forces the agent to leverage statistical patterns about typical costs, transit times, and attraction popularity rather than accessing ground truth. The Reviewer then serves as a validation layer, essentially performing an adversarial audit through internet fact-checking. 

The primary challenge.

At first the Reviewer agent didn't use the tool calling functionality. Initial iterations produced verbose feedback without tool calls, essentially creating two Planners with different personas. I addressed this by explicitly instructing the Reviewer to "use the internet_search tool liberally and strategically" and structuring its output format around a Delta List that requires cited sources. The specificity of requesting factual verification for opening hours, current pricing, and transit times created natural trigger points for tool usage.

My design approach emphasized asymmetric information access between agents. The Planner received detailed instructions about structure, logistics, and user constraint handling to maximize its output quality given its knowledge limitations. The Reviewer received shorter, more directive instructions focused on systematic validation rather than creative planning. This separation of concerns prevents the Reviewer from overstepping into redesigning the entire itinerary while ensuring it catches factual errors.

One interesting observation involved the tradeoff between agent creativity and reliability. Giving the Planner more detailed structural requirements reduced variability in output format but occasionally constrained its ability to propose unconventional itineraries. Similarly, the Reviewer's aggressive fact-checking sometimes flagged minor discrepancies that wouldn't materially impact trip feasibility. Balancing these tensions required iterative refinement of both instruction sets to achieve useful collaboration without excessive friction between agents.

External Tools and Assistance:

GPT5 was used to help draft and refine the ref-log.md for grammar and other enhancements of language.