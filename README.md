# Dog Care Agent

This is a RAG based agent built using PREM tools and the Fetch.ai uagents. It provides information about dog care.

## Example input

```python
message="what are some common intestinal parasites in dogs?"
```

## Example output

```
Common intestinal parasites in dogs include:

1. **Tapeworms**: Typically contracted by ingesting fleas that carry tapeworm eggs. Once inside the dog's intestine, the tapeworm hatches and attaches itself to the intestinal lining.

2. **Hookworms**: These parasites attach to the dog's intestinal lining with hook-like teeth and feed on their blood. They can be transmitted through ingestion or by penetrating the dog's skin.

3. **Roundworms**: Often found in puppies, who can be born with them or acquire them through their mother's milk. Older dogs can become infected through contact with soil containing roundworm eggs.

4. **Whipworms**: Live in the large intestine and cecum of the dog, causing symptoms such as diarrhea, weight loss, and dehydration.

Each type of worm can have serious health implications for dogs, requiring prompt diagnosis and treatment.

```
Read the [Medium article](https://medium.com/@kshipra.dhame/building-a-rag-based-ai-agent-for-dog-care-with-prem-and-fetch-ai-0837a86633b4) to understand the deployment process.


1. Install the necessary packages:

   ```bash
   pip install requests uagents
   ```

2. You can get the PREM API key please visit [PREM](https://app.premai.io/accounts/signup/). 

3. Run the agent:
   ```bash
   python dogcare-agent.py
   ```

