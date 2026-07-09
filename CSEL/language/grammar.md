# CSEL-0000: Language Grammar & Syntax

## 1. Objective
To define the formal syntax rules, keyword definitions, and token guidelines for the Cognitive Systems Engineering Language (CSEL), establishing a declarative scientific layout.

---

## 2. Language Keywords

CSEL utilizes block-based keywords to define system structures and operations:

* **`ENTITY`**: Registers a new cognitive object.
* **`TYPE`**: Specifies the CTS type of the entity.
* **`IDENTITY`**: Declares the permanent `cse://` namespace identifier.
* **`CONSTRAINTS`**: Defines rules that must be satisfied for compilation.
* **`TRANSFORMATION`**: Mapped equation describing state updates.
* **`INVARIANT`**: Absolute constraints that cannot be breached.
* **`EVIDENCE`**: References to validated evidence or experimental test results.
* **`CONFIDENCE`**: The epistemic score of the entity.
* **`LINEAGE`**: Provance history references.

---

## 3. Structural Syntax Specification

CSEL objects are declared using block-notation with colon-value properties:

```csel
ENTITY [Name] {
    
    TYPE:
        [CTS-Type-Class]
        
    IDENTITY:
        cse://[domain]/[path]
        
    [PROPERTY_KEY]:
        [Value, Equation, or List]
}
```

### Grammar Rules:
1. **Identifier Scope**: Every name must resolve to a valid namespace structure in `cse://`.
2. **Structural Block Constraints**: Braces `{}` separate scope levels. Key names are followed by a colon and indented properties.
3. **Expression Format**: Transformation equations are declared using relational operators (e.g. `Signal + Context => Belief`).

---

## 4. Parser Token Grammar (EBNF)

The compiler tokenizes CSEL inputs using the following formal grammar rules:

```ebnf
EntityBlock    ::= "ENTITY" Identifier "{" PropertyList "}"
PropertyList   ::= Property*
Property       ::= PropertyKey ":" Value
PropertyKey    ::= "TYPE" | "IDENTITY" | "CONSTRAINTS" | "TRANSFORMATION" | "INVARIANT" | "EVIDENCE" | "CONFIDENCE" | "LINEAGE"
Identifier     ::= [a-zA-Z_][a-zA-Z0-9_]*
Value          ::= String | URI | List | Expression
Expression     ::= Identifier ( "+" Identifier )* "=>" Identifier
URI            ::= "cse://" [a-zA-Z0-9_\-\./]+
List           ::= ( "-" Value )+
```
