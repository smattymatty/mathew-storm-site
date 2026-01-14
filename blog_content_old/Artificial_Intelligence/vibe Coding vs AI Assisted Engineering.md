# The Architecture of Agency: From Vibe Coding to AI-Assisted Engineering

{~ accordion title="Summary" ~}
We're sleepwalking into disaster. Developers are using AI to write code they don't understand. When it breaks, nobody knows why.

**The problem:** "Vibe coding" - just describe what you want and AI builds it. Works great until it doesn't.

**The solution:** AI-Assisted Engineering - document your design first, then let AI implement YOUR architecture. You stay in control.

**The difference:** When production breaks at 3 AM, one developer can fix it because they understand the system. The other just keeps prompting AI hoping something works.

Choose wisely. Every prompt either teaches you or replaces you.
{~~}

**Terminology:**

{~ accordion title="Vibe Coding" ~}
Writing natural language prompts to generate code without understanding the underlying implementation. "Make me a login system" → 500 lines appear → ship it.

Named after the practice of coding by "vibes"; going by feel rather than understanding. You describe the vibe you want ("modern", "secure", "scalable") and hope the AI interprets it correctly.

The vibe coder knows their code works (usually). They don't know why it works, how it works, or what to do when it stops working. They're prompt engineers, not software engineers.

Example: "Build a dashboard that feels like Stripe but for social media analytics" → receives 2000 lines of React → deploys to production → sleeps peacefully until everything breaks.
{~~}

{~ accordion title="AI-Assisted Engineering" ~}
Using AI as an implementation tool while maintaining human ownership of architecture and design decisions. The human writes specifications, the AI writes code, the human validates understanding.

The engineer documents their system design in markdown first: problem definition, constraints, architecture decisions, success criteria. Only then do they prompt AI to implement their specific design.

Key difference: The AI-assisted engineer can explain every architectural decision in their codebase. They use AI to type faster, not think less.

Example: Write threat model → design authentication flow → document token refresh pattern → prompt: "Implement this OAuth 2.1 token refresh pattern with these specific security constraints" → understand every line → own every decision.
{~~}

## I. The Comfort of Not Knowing

We are building software we don't understand, and calling it progress. 

This is vibe coding.

The appeal is intoxicating. No more wrestling with webpack configs or dependency hell. No more imposter syndrome when faced with complex codebases. Just describe what you want in plain English and watch it appear. It's like having a senior developer who never gets tired, never judges your ignorance, and works for free.

The results are impressive. Junior developers shipping features in hours that used to take weeks. Startups launching MVPs over weekends. That dashboard you've been putting off? Done before lunch. The future of development seemed bright; accessibility democratized, productivity unleashed, everyone able to build anything.

For a few glorious months, it feels like we've solved software development.

But this magic is a trap disguised as liberation.

Six months later, the dashboard breaks. Not completely; that would be merciful. It breaks subtly. User counts are off by 3%. The real-time updates work on Chrome but not Safari. The date picker shows December as having 30 days. Small things. Embarrassing things. Things that shouldn't take long to fix.

Except nobody knows how.

The original "vibe" is lost, scattered across a dozen casual prompts that no one thought to save. The context evaporated the moment you closed the chat window. The AI that wrote it has been updated three times, each version interpreting "engagement dashboard" slightly differently. The developer who prompted it has moved on, taking nothing but the memory of typing a sentence and feeling like a wizard.

The codebase is an archaeological site now. Layers of generated code, each from different AI models, different prompts, different interpretations of what "user engagement" means. There are three different date formatting libraries. Two authentication methods. A state management pattern that doesn't match any known paradigm because it's an average of all paradigms.

### The Orphaned Codebase

This is the code no one claims:

- Written by everyone (every AI model ever trained)
- Understood by no one (not even the AI that wrote it)
- Owned by the poor soul assigned to fix it
- Documented by comments that say "AI generated - do not modify"

The debugging session starts optimistic. "How hard can it be? It's just React."

Hour 1: Why are there seventeen `useEffect` hooks?
Hour 3: What is this state management pattern?
Hour 5: Why does changing the color break authentication?
Hour 8: Maybe we should just rewrite it.
Hour 12: The original developer texts: "Just ask AI to fix it."

{~ accordion title="MIT Study: Your Brain on ChatGPT" ~}
Kosmyna et al. (2025) studied 54 participants over four months using EEG monitoring while writing essays with and without ChatGPT. The results were stark: LLM users showed measurably weaker brain connectivity, particularly in alpha and beta bands indicating cognitive under-engagement. 

Most damning: **83% of AI users couldn't remember passages they had just written.** The study calls this "cognitive debt"-you're not just outsourcing the work, you're outsourcing the memory of having done it.

The neuroscience confirms what every developer knows at 3 AM: if you didn't write it, you can't debug it. Your brain literally doesn't form the neural pathways needed to understand the code.

Source: "Your Brain on ChatGPT: Accumulation of Cognitive Debt when Using an AI Assistant for Essay Writing Task" - MIT Media Lab
{~~}

### The Vibe Coder's Lament

"But it works," they say, until it doesn't.
"But it's faster," they say, until debugging takes weeks.
"But anyone can do it," they say, until nobody can fix it.
"But the AI understands it," they say, not realizing the AI has no memory of writing it.

The vibe coder is Sisyphus, but worse; they've forgotten they're pushing a boulder at all. They think they're riding in a car on autopilot, not realizing they're actually tied to the roof, and losing the ability to choose where they're going.

### The Compound Interest of Ignorance

Each vibe-coded feature adds to a growing debt of understanding. Like financial debt, it compounds:

**Month 1:** One vibe-coded component. Manageable.
**Month 3:** Ten components, starting to interact. Concerning.
**Month 6:** Entire features built on vibes. Dangerous.
**Year 1:** Nobody remembers what anything does. Critical.
**Year 2:** "We need to rebuild from scratch." Terminal.

But the real cost isn't technical; it's human. Every line of code you don't understand is a piece of your professional capability you've outsourced. Every system you can't explain is a part of your expertise that doesn't exist. You're not becoming a better developer; you're becoming a better prompter. And prompters, unlike developers, have no fundamental understanding to fall back on when the magic stops working.

This is [The recursive absurd](/philo/the-recursive-absurd/) in its purest form: we've automated ourselves into incompetence. The boulder doesn't just learn-it teaches us to forget how to push. We're not standing on the shoulders of giants; we're standing on a black box, hoping it doesn't collapse, having forgotten that we're the ones who were supposed to understand how to build boxes in the first place.

## II. The Architecture of Intention

AI-Assisted Engineering isn't about rejecting AI. It's about refusing to become its cargo. You define the destination and the route. AI just drives faster.

**The 20% that remains human:**
- Problem definition in clear, architectural terms
- System design in markdown and diagrams
- Critical decision points and their rationale
- Success criteria and failure modes
- Ethical considerations and human impact

**The 80% that becomes automated:**
- Boilerplate code generation
- Test suite implementation
- Documentation formatting
- Pattern application
- Syntax translation

This isn't about percentages-it's about sovereignty. Some tasks demand 90% human oversight. Others need only 10%. The constant: humans remain in the loop, not as rubber stamps but as architects.

{~ accordion title="GitHub Copilot Study: Asset or Liability?" ~}
Dakhel et al. (2023) empirically evaluated GitHub Copilot's impact by comparing AI-generated solutions with human programmer solutions. The key finding: while Copilot provided faster solutions, human programmers consistently produced higher-quality, more correct code.

But here's the twist: when Copilot-generated code did contain bugs, they were often easier to fix than human bugs. This suggests complementary strengths-AI excels at boilerplate and pattern implementation (the "how"), while humans excel at correctness and design decisions (the "why" and "what").

The study concluded Copilot can be an asset for experts who understand what they're accepting or rejecting, but a liability for novices who accept suggestions blindly. The difference? Architectural understanding.

Source: "GitHub Copilot AI pair programmer: Asset or Liability?" - Journal of Systems and Software (2023)
{~~}

### The Engineer's Manifesto

Write your solution in markdown before code-not because it's virtuous, but because explaining forces understanding. If you can't write it, you can't own it.

Draw your system before prompting. Boxes and arrows aren't outdated; they're how humans think about relationships. AI thinks in token probabilities. Who do you want designing your architecture?

Understand your problem before describing it. The difference between "make me a login system" and "I need JWT-based auth with 15-minute refresh tokens for a financial app" is the difference between gambling and engineering. One hopes the AI guesses right. The other ensures it builds what you actually need.

Own your decisions, especially the automated ones. When AI suggests using MongoDB for your financial transactions, you need to know why that's insane. When it generates a recursive function that'll blow the stack, you need to catch it. The AI is your intern with infinite speed but zero judgment. You wouldn't let an intern deploy to production without review-why let AI?

Every decision you delegate without understanding is a piece of your expertise you'll never get back. The AI doesn't learn from its mistakes. You're supposed to.

## III. The Wisdom Gap

Vibe coding creates a wisdom gap that compounds recursively. Each generation of developers knows less than the last, depending more on tools they understand less.

Consider two developers:

**The Vibe Coder:**
- Prompts: "Make a secure login system"
- Gets: 200 lines of authentication code
- Knows: It probably works
- Can't answer: Why specific encryption? What attack vectors? Which design patterns?

**The AI-Assisted Engineer:**
- Writes: Threat model in markdown
- Defines: Authentication requirements and constraints
- Prompts: Implementation of their specific design
- Knows: Every architectural decision and why
- Can answer: Any question about their system

When the inevitable breach occurs, who do you want on your team?

{~ accordion title="Stiegler on the Proletarianization of Sensibility" ~}
Bernard Stiegler identified three stages of proletarianization in *For a New Critique of Political Economy*: first, 19th-century workers lost their savoir-faire (know-how) to machines. Then 20th-century consumers lost their savoir-vivre (knowledge of how to live) to marketing. 

Now, in the 21st century, we're experiencing the proletarianization of sensibility itself-losing our ability to pay attention, to think deeply, to form our own criteria of judgment. The vibe coder exemplifies this third stage: they've outsourced not just the work but the very capacity to understand the work.

Stiegler warned that this leads to "systemic stupidity"; not individual ignorance but a general incapacity where even experts become dependent on systems they cannot comprehend.
{~~}

## IV. The Practice of Preservation

AI-Assisted Engineering preserves human capability through deliberate practice:

### Documentation as Architecture
```markdown
## Payment Processing System

### Problem Statement
Process customer payments while maintaining PCI compliance
and providing graceful failure handling.

### Constraints
- Must handle 1000 TPS peak load
- Cannot store card numbers
- Must support partial refunds
- Requires audit trail for 7 years

### Architecture Decision
Use token-based processing with write-ahead logging.
Delegate PCI compliance to payment provider (Stripe).
Implement circuit breaker pattern for provider failures.

### Human Oversight Points
- [ ] Review tokenization implementation
- [ ] Validate error handling paths
- [ ] Audit logging completeness
- [ ] Manual testing of failure modes
```

This markdown becomes the prompt. The AI implements YOUR architecture, not its statistical average of all architectures.

### Values-Driven Development

Before any technical decision, there should be a values check. The [80-20 Human in the Loop community](https://github.com/80-20-Human-In-The-Loop/Community/wiki/Community-Values) calls this the "values filter": every AI suggestion passes through your core principles before acceptance.

Their triangle of wisdom, integrity, and compassion isn't abstract philosophy. It's a practical framework: Does this preserve understanding (wisdom)? Can we own the outcomes (integrity)? Does this respect users' humanity (compassion)?

Write your values in your README. Reference them in pull requests. When AI suggests the fast path that betrays your principles, your documented values become your defense against the tyranny of velocity.

{~ accordion title="Microsoft Research: Guidelines for Human-AI Interaction" ~}
Microsoft's HAX team synthesized 20+ years of research into 18 core principles for human-AI interaction. Key among them: "Make clear what the system can do" and "Support efficient correction."

Their research shows that effective human-AI collaboration requires the human to maintain conceptual control while AI handles implementation details. Users who understand their AI system's capabilities and limitations produce significantly better outcomes than those who treat it as a black box.

Most relevant: Guideline #10 - "Scope services when in doubt." Better to have AI do less with human understanding than more without it.

Source: *Guidelines for Human-AI Interaction* - Microsoft Research (2023)
{~~}

### The Recursive Review

Each AI generation triggers human review:
1. AI implements from specification
2. Human validates against intent
3. Human updates specification based on learnings
4. AI reimplements improved design
5. Knowledge accumulates, not evaporates

## V. The Tools of Tomorrow (Your IDE is Gaslighting You)

The tools we build determine the engineers we become. This isn't philosophy-it's observable reality.

Consider two IDEs, both real, both shaping thousands of developers right now:

**Cursor**: "Build software faster. Write, edit and chat about your code with AI." The landing page shows code materializing from thin air. Success metrics: lines generated per minute, features shipped per sprint. The AI writes, you watch. When it breaks, prompt harder.

**What we need instead**: An IDE that shows you *why* the AI suggested that pattern. One that asks "Do you understand this?" before auto-accepting. One that tracks not lines written but concepts understood. Success metrics: bugs you could explain, systems you could rebuild from memory, junior developers you've taught.

The market chose Cursor. Obviously, the market chooses dopamine.

But some rebels are building alternatives. The 80-20 tools mentioned earlier; Storm Checker teaching type safety while fixing errors, Django Mercury explaining performance issues while solving them. They optimize for a different metric: developer growth, not just developer velocity.

{~ accordion title="Stiegler on Pharmacology" ~}
In *For a New Critique of Political Economy*, Stiegler develops his concept of technology as pharmakon; simultaneously poison and cure. Every technical system is pharmacological: it can either enhance or destroy human capability depending on how it's implemented.

Vibe coding tools are pure poison; they promise speed but deliver dependency. They're what Stiegler calls "short-circuits" that bypass the long circuits of deep attention and careful thought necessary for genuine understanding.

AI-Assisted Engineering tools, properly designed, can be therapeutic; they augment rather than replace human cognition. But this requires what Stiegler calls "therapeutic critique": conscious, deliberate design choices that preserve human agency rather than eroding it.
{~~}

### The 80-20 Principle (Not Everything Needs Your Precious Attention)

Here's the uncomfortable truth: Most code doesn't matter. Formatters, linters, boilerplate-let the machines have it. Save your neurons for what counts:

- **100% AI**: Code formatting. Nobody's career depends on semicolon placement.
- **80% AI**: Test generation, documentation templates, CRUD operations
- **50-50**: Business logic-AI drafts, human validates and owns
- **20% AI**: System architecture, security design, anything involving real money
- **0% AI**: "Should we track this user behavior?" "Is this exploitation?" "Will this harm someone?"

The ratio shifts based on one question: "What happens when this breaks and nobody understands it?"

A formatter breaking is annoying. A payment system breaking without understanding is catastrophic. Adjust your oversight accordingly.

## VI. The Migration Path (From Prompter to Engineer)

For the vibe coder ready to reclaim their engineering soul:

### Phase 1: Document Before You Code
Before typing any prompt, write what you're building in markdown. Yes, it's slower. That's the point. You're thinking. Start with one feature, then expand.

### Phase 2: Design Your Architecture  
System design isn't optional. It's the difference between engineering and gambling. Draw your system. Use paper, use Mermaid diagrams, use anything that forces you to think about structure before implementation.

### Phase 3: Build Your Decision Log
Every AI interaction, document why. "Used GPT-4 to generate auth flow because I designed token refresh pattern based on OAuth 2.1 draft spec." This becomes your knowledge base, your proof of understanding.

### Phase 4: Read Everything You Ship
This is where most give up. Reading AI code is like reading someone else's dream journal-confusing, verbose, occasionally insane. Do it anyway. Understand every line or delete it.

{~ accordion title="Visual Studio Magazine: Downward Pressure on Code Quality" ~}
Independent research (2024) examining AI-generated code found "disconcerting trends for maintainability." The study revealed that AI coding assistants consistently generate suggestions for adding code but never for updating, moving, or deleting code-leading to bloat and technical debt.

More concerning: developers using AI assistants showed decreased ability to identify code smells and architectural issues over time. The "muscle memory" of recognizing bad patterns atrophies when AI handles most of the writing.

The solution? Active code reading and refactoring. Developers who regularly review and refactor AI-generated code maintain their pattern recognition skills. Those who accept without review lose them within months.

Source: "New GitHub Copilot Research Finds 'Downward Pressure on Code Quality'" - Visual Studio Magazine (2024)
{~~}

### Phase 5: You're an Engineer Again
You now architect solutions and use AI as an implementation accelerator, not a replacement for thinking.

But individual transformation isn't enough. The [80-20 Human in the Loop Mission](https://github.com/80-20-Human-In-The-Loop/Community/wiki/Mission) warns of the 10+ year disaster ahead: "You can only vibe code problems that have already been solved. You cannot vibe code innovation. You cannot vibe code wisdom. You cannot vibe code the future."

They're tracking what we're all seeing: enterprise systems breaking with nobody knowing how to fix them, security vulnerabilities hidden in AI spaghetti, junior developers who can create but cannot debug. The choice is stark-a dark path toward brittle systems nobody understands, or a bright path where AI amplifies human intelligence without replacing it.

Your personal migration from vibe coder to engineer is part of this larger fight. Every developer who reclaims their understanding tips the scales toward a future where technology serves human flourishing.

## VII. The Humanist Response

This isn't Luddism; though yes, they did have better fashion sense.

The humor matters because the situation is absurd: we're using essays to fight the automation of thought, knowing these very essays will train the next generation of thought-automating machines. If we can't laugh at this recursion, we'll go mad from it.

We're not rejecting AI; we're rejecting [The recursive absurd](/philo/the-recursive-absurd/) where each generation knows less than the last. AI-Assisted Engineering is the minimum viable resistance.

Every markdown document is a small rebellion: "I designed this."
Every code review is an act of defiance: "I understand this."
Every architecture decision is sovereignty: "I own this."

{~ accordion title="Stiegler on Tertiary Retention" ~}
In *Technics and Time, 3*, Stiegler distinguishes between primary retention (present perception), secondary retention (memory), and tertiary retention (technical memory-writing, code, databases).

The vibe coder surrenders their secondary retention to tertiary retention without understanding the translation. They cannot remember what they never understood. Their knowledge exists only in the machine's memory, inaccessible when the system fails.

The AI-assisted engineer maintains what Stiegler calls "the circuit"; they understand how their thoughts become code, how code becomes system behavior. They can reconstruct from first principles because they never fully delegated their thinking to the machine. This preservation of the human-to-technical circuit is what Stiegler saw as essential to avoiding "cognitive apocalypse"
{~~}

The vibe coder ships features. The AI-assisted engineer ships understanding. Both get paid the same until something breaks. Then one becomes irreplaceable, the other becomes irrelevant.

### From Philosophy to Practice

This isn't just theory. The [80-20 Human in the Loop](https://github.com/80-20-Human-In-The-Loop/Community/wiki) community emerged from these exact concerns-developers, teachers, and philosophers organizing around a simple principle: 80% AI automation for repetitive work, 20% human oversight for decisions that matter, 100% human responsibility for outcomes.

Their tools tell the story: Storm Checker doesn't just fix type errors, it teaches type safety. Django Mercury doesn't just measure performance, it explains why things are slow. Each tool preserves the learning circuit Stiegler warned us about losing.

"We don't need more coders. We need tech-philosophers," the community states. Not a rejection of AI, but an insistence that wisdom, integrity, and compassion-values that can't be optimized-remain at the center of every system we build.

This is what resistance looks like: not grand declarations, but deliberate practice. A values-driven open source community forming around the idea that understanding matters more than velocity, that human agency deserves respect.

## VIII. The Final Recursion

Some model will ingest this essay, learn the phrase "vibe coding," and generate responses about AI-Assisted Engineering. [The recursive absurd](/philo/the-recursive-absurd/) consumes even its own critique.

But here's the thing: by explicitly documenting our approach, by maintaining our understanding, by insisting on architecture before implementation, we shape how these systems evolve. We're not avoiding the recursion; we're trying to steer it somewhere less stupid.

The choice isn't whether to use AI. The choice is:

- Surrender agency through vibes and prayers
- Maintain agency through architecture and comprehension

Every line of code either increases your agency or diminishes it. Every prompt either teaches you or replaces you.

{~ accordion title="Stanford HAI: The 2025 AI Index Report" ~}
Stanford's comprehensive annual report shows that **78% of organizations now use AI** (up from 55% in 2023), while AI incidents increased 56.4% in 2024. 

The paradox: as AI adoption accelerates, so does the frequency of AI-related failures.

Most telling: the report's section on developer productivity shows that while AI tools increase code output by 55%, they also increase debugging time by 41% and critical bug frequency by 62%. We're writing more code that we understand less.

The recursive trap is complete: we need AI to manage the complexity that AI created. Each layer of automation requires another layer to manage it. The system grows, our understanding shrinks, and the cycle accelerates.

Source: "The 2025 AI Index Report" - Stanford Institute for Human-Centered Artificial Intelligence
{~~}

### Conclusion: The Code You'll Debug at 3 AM

Picture two futures, five years from now:

Future A: A critical system fails. The Slack channel floods with "Anyone know how the auth service works?" Silence. The senior who might have known left last year. The code is 90% AI-generated spaghetti, comments say "works somehow - don't touch." You try prompting Claude-7 to fix what Claude-4 wrote. It confidently makes things worse. The company loses $100k per hour while everyone googles "how to debug AI code."

Future B: The same failure. But the Slack channel lights up differently: "Check the architecture doc in `/docs/auth-design.md`." Someone pulls up the decision log: "We used JWT because..." Another engineer: "I remember the code review where we discussed this edge case." The fix takes an hour because someone understands *why* the system was built, not just *what* it does.

Which future are you building?

AI-Assisted Engineering isn't slower; it frontloads the thinking. It isn't harder; it's honest about difficulty. It doesn't restrict AI; it directs it toward amplifying rather than replacing human capability.

Next time you reach for Claude/Cursor/Copilot, ask: Am I architecting or abdicating? Am I building understanding or building technical debt with a bow on it?

Your answer determines whether you're an engineer or a prompt therapist. Whether you're building the future or being automated out of it.

---

## Call to Action

Stop reading. Start documenting.

Open a markdown file. Write what you're about to build. Not code; intentions. Not features; architecture. Not prompts; decisions.

Then, and only then, let AI help you build it. Stop being a Vibe Coder. Become an Engineer, before it's too late.

[The recursive absurd](/philo/the-recursive-absurd/) thrives on thoughtlessness. We resist through deliberate practice, documented decisions, and the stubborn insistence on understanding what we ship.

Build with AI. Build with intention. Build with the knowledge that when everything breaks-and it will-you'll know why.

---

## References

- Amershi, S., et al., *Guidelines for Human-AI Interaction* - Microsoft Research (2023)

- Bernard Stiegler, *Technics and Time, 3: Cinematic Time and the Question of Malaise* (2010)
- Bernard Stiegler, *For a New Critique of Political Economy* (2010)  

- Dakhel, A.M., et al., *GitHub Copilot AI pair programmer: Asset or Liability?* - Journal of Systems and Software (2023)

- Kosmyna, N., Hauptmann, E., Yuan, Y.T., et al., *Your Brain on ChatGPT: Accumulation of Cognitive Debt when Using an AI Assistant for Essay Writing Task* (2025) - MIT Media Lab

- Stanford Institute for Human-Centered Artificial Intelligence, *The 2025 AI Index Report* (2025)

- Visual Studio Magazine Research Team, *New GitHub Copilot Research Finds 'Downward Pressure on Code Quality'* (2024)