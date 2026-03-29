# Diagrams

This page collects the visual diagrams used by the repository.

本页集中存放仓库里的示意图，方便单独引用或后续补充。

## System Architecture | 系统架构

```mermaid
flowchart LR
    A["Job Source"] --> B["Normalizer"]
    B --> C["Stable Identity Builder"]
    C --> D["State Store"]
    D --> E["Scoring + Planner"]
    E --> F["Auto Greet Gate"]
    F --> G["Greeting Action"]
    G --> H["Reply Watcher"]
    H --> I["Reply Trigger Gate"]
    I --> J["Tailored Resume Bundle"]
    J --> K["Browser Sender"]
    K --> L["Success State / Fallback Notify"]
```

## Job Lifecycle | 岗位生命周期

```mermaid
stateDiagram-v2
    [*] --> Seen
    Seen --> New: first merge
    New --> Greeted: greet success
    New --> Blocked: greet rejected code=1
    New --> Skipped: manual skip
    Greeted --> Replied: first recruiter reply
    Replied --> ResumeSent: auto send success
    Replied --> ManualFallback: auto send failed
    Blocked --> [*]
    ResumeSent --> [*]
    ManualFallback --> [*]
    Skipped --> [*]
```

## First Reply Decision | 首次回复判定

```mermaid
flowchart TD
    A["Recruiter reply arrives"] --> B{"greeted_at exists?"}
    B -- No --> X["Ignore"]
    B -- Yes --> C{"fingerprint changed?"}
    C -- No --> X
    C -- Yes --> D{"resume_sent_at exists?"}
    D -- Yes --> X
    D -- No --> E["Generate resume + draft"]
```
