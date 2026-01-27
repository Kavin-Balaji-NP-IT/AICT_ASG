from typing import Set, List, Tuple, Dict, Optional
from itertools import combinations
import copy

from logic_rules_data import (
    SYMBOL_DEFINITIONS,
    LOGICAL_RULES,
    TEST_SCENARIOS,
    FUTURE_ONLY_STATIONS,
    FUTURE_ONLY_LINES,
)


class Clause:
    """Represents a clause in CNF (Conjunctive Normal Form)"""
    
    def __init__(self, literals: Set[str]):
        """
        Initialize clause with a set of literals
        Literals are strings, negated literals start with '~'
        """
        self.literals = frozenset(literals)
    
    def __eq__(self, other):
        return isinstance(other, Clause) and self.literals == other.literals
    
    def __hash__(self):
        return hash(self.literals)
    
    def __repr__(self):
        if not self.literals:
            return "[]"  # Empty clause (contradiction)
        return " ∨ ".join(sorted(self.literals))
    
    def __bool__(self):
        """Empty clause is False (represents contradiction)"""
        return len(self.literals) > 0
    
    def is_unit_clause(self) -> bool:
        """Check if clause has exactly one literal"""
        return len(self.literals) == 1
    
    def get_literal(self) -> Optional[str]:
        """Get the single literal (for unit clauses)"""
        if self.is_unit_clause():
            return next(iter(self.literals))
        return None


class KnowledgeBase:
    """Represents a knowledge base in propositional logic"""
    
    def __init__(self):
        self.clauses: Set[Clause] = set()
        self.facts: Set[str] = set()
    
    def add_fact(self, fact: str):
        """Add a fact (unit clause) to the knowledge base"""
        self.facts.add(fact)
        self.clauses.add(Clause({fact}))
    
    def add_rule(self, premises: List[str], conclusion: str):
        """
        Add a rule to the knowledge base
        Rule: premises => conclusion
        CNF form: ~premise1 ∨ ~premise2 ∨ ... ∨ conclusion
        """
        clause_literals = {conclusion}
        for premise in premises:
            # Negate each premise
            if premise.startswith('~'):
                clause_literals.add(premise[1:])
            else:
                clause_literals.add('~' + premise)
        
        self.clauses.add(Clause(clause_literals))
    
    def add_clause(self, clause: Clause):
        """Add a clause directly to the knowledge base"""
        self.clauses.add(clause)
    
    def negate_symbol(self, symbol: str) -> str:
        """Negate a symbol"""
        if symbol.startswith('~'):
            return symbol[1:]
        return '~' + symbol
    
    def resolve(self, clause1: Clause, clause2: Clause) -> Set[Clause]:
        """
        Perform resolution between two clauses
        Returns set of resolvent clauses (may be empty if no resolution possible)
        """
        resolvents = set()
        
        # Try to resolve on each pair of complementary literals
        for lit1 in clause1.literals:
            neg_lit1 = self.negate_symbol(lit1)
            
            if neg_lit1 in clause2.literals:
                # Found complementary pair, create resolvent
                new_literals = (clause1.literals | clause2.literals) - {lit1, neg_lit1}
                resolvents.add(Clause(new_literals))
        
        return resolvents
    
    def pl_resolution(self, query: str, max_iterations: int = 1000) -> Tuple[bool, List[str]]:

        # Negate the query and add to KB
        negated_query = self.negate_symbol(query)
        temp_kb = copy.deepcopy(self)
        temp_kb.add_clause(Clause({negated_query}))
        
        clauses = temp_kb.clauses
        new_clauses = set()
        proof_trace = []
        iteration = 0
        
        while iteration < max_iterations:
            iteration += 1
            clause_pairs = list(combinations(clauses, 2))
            
            if not clause_pairs:
                break
            
            for clause1, clause2 in clause_pairs:
                resolvents = temp_kb.resolve(clause1, clause2)
                
                for resolvent in resolvents:
                    # Check if we derived empty clause (contradiction)
                    if not resolvent:
                        proof_trace.append(f"Derived empty clause from {clause1} and {clause2}")
                        proof_trace.append(f"Therefore, {query} is TRUE")
                        return True, proof_trace
                    
                    new_clauses.add(resolvent)
                    if resolvent not in clauses:
                        proof_trace.append(f"Resolved {clause1} and {clause2} → {resolvent}")
            
            # Check if no new clauses were derived
            if new_clauses.issubset(clauses):
                proof_trace.append(f"No new clauses derived. {query} cannot be proven.")
                return False, proof_trace
            
            clauses = clauses | new_clauses
        
        proof_trace.append(f"Max iterations reached. {query} cannot be proven.")
        return False, proof_trace
    
    def check_consistency(self) -> Tuple[bool, Optional[str]]:

        clauses = copy.deepcopy(self.clauses)
        new_clauses = set()
        
        max_iterations = 500
        iteration = 0
        
        while iteration < max_iterations:
            iteration += 1
            clause_pairs = list(combinations(clauses, 2))
            
            if not clause_pairs:
                break
            
            for clause1, clause2 in clause_pairs:
                resolvents = self.resolve(clause1, clause2)
                
                for resolvent in resolvents:
                    if not resolvent:  # Empty clause = contradiction
                        explanation = f"Contradiction found: {clause1} and {clause2} resolve to empty clause"
                        return False, explanation
                    
                    new_clauses.add(resolvent)
            
            if new_clauses.issubset(clauses):
                return True, None
            
            clauses = clauses | new_clauses
        
        return True, None  # Couldn't find contradiction


class LogicInferenceSystem:
    
    def __init__(self):
        self.rules = LOGICAL_RULES
        self.symbol_definitions = SYMBOL_DEFINITIONS
    
    def create_kb_from_facts(self, facts: List[str]) -> KnowledgeBase:
        
        kb = KnowledgeBase()
        
        # Add all rules to KB
        for rule in self.rules:
            kb.add_rule(rule["premises"], rule["conclusion"])
        
        # Add facts
        for fact in facts:
            kb.add_fact(fact)
        
        return kb
    
    def check_scenario_validity(self, scenario: Dict) -> Dict:

        facts = scenario["facts"]
        kb = self.create_kb_from_facts(facts)
        
        # Check consistency
        is_consistent, contradiction = kb.check_consistency()
        
        result = {
            "scenario_id": scenario["id"],
            "scenario_name": scenario["name"],
            "is_valid": is_consistent,
            "facts": facts,
            "violated_rules": [],
            "inferences": [],
            "explanation": ""
        }
        
        if not is_consistent:
            result["explanation"] = contradiction
            result["violated_rules"] = self._identify_violated_rules(facts)
        else:
            # Find inferences
            result["inferences"] = self._find_inferences(kb, facts)
            result["explanation"] = "Scenario is consistent with all rules"
        
        return result
    
    def _identify_violated_rules(self, facts: List[str]) -> List[str]:

        violated = []
        
        for rule in self.rules:
            # Check if premises are satisfied but conclusion is violated
            premises_satisfied = all(premise in facts for premise in rule["premises"])
            
            conclusion = rule["conclusion"]
            conclusion_violated = False
            
            if conclusion.startswith('~'):
                # Conclusion is negated, check if positive version is in facts
                positive = conclusion[1:]
                conclusion_violated = premises_satisfied and positive in facts
            else:
                # Conclusion is positive, check if negated version is in facts
                negated = '~' + conclusion
                conclusion_violated = premises_satisfied and negated in facts
            
            if conclusion_violated:
                violated.append(rule["id"])
        
        return violated
    
    def _find_inferences(self, kb: KnowledgeBase, known_facts: List[str]) -> List[str]:

        inferences = []
        
        # Get all symbols mentioned in rules
        all_symbols = set()
        for rule in self.rules:
            all_symbols.update(rule["premises"])
            all_symbols.add(rule["conclusion"].replace('~', ''))
        
        # Try to prove each symbol
        for symbol in all_symbols:
            if symbol not in known_facts and f'~{symbol}' not in known_facts:
                # Try to prove positive
                can_prove_positive, _ = kb.pl_resolution(symbol)
                if can_prove_positive:
                    inferences.append(symbol)
                    continue
                
                # Try to prove negative
                can_prove_negative, _ = kb.pl_resolution(f'~{symbol}')
                if can_prove_negative:
                    inferences.append(f'~{symbol}')
        
        return inferences
    
    def explain_rule(self, rule_id: str) -> str:
        for rule in self.rules:
            if rule["id"] == rule_id:
                return f"{rule['id']}: {rule['plain_english']}"
        return f"Rule {rule_id} not found"
    
    def explain_symbol(self, symbol: str) -> str:
        clean_symbol = symbol.replace('~', '')
        if clean_symbol in self.symbol_definitions:
            meaning = self.symbol_definitions[clean_symbol]
            if symbol.startswith('~'):
                return f"NOT ({meaning})"
            return meaning
        return f"Symbol {symbol} not defined"


def print_scenario_result(result: Dict, verbose: bool = True):
    """Pretty print scenario test result"""
    print(f"\n{'='*79}")
    print(f"Scenario {result['scenario_id']}: {result['scenario_name']}")
    print(f"{'='*79}")
    
    print(f"\nStatus: {'✓ VALID' if result['is_valid'] else '✗ INVALID'}")
    
    print(f"\nGiven Facts:")
    for fact in result['facts']:
        print(f"  • {fact}")
    
    if result['is_valid']:
        if result['inferences']:
            print(f"\n✓ Inferred Facts:")
            for inference in result['inferences']:
                print(f"  • {inference}")
        else:
            print(f"\n(No additional inferences beyond given facts)")
    else:
        print(f"\n✗ Violated Rules: {', '.join(result['violated_rules'])}")
        print(f"✗ Explanation: {result['explanation']}")
    
    if verbose:
        print(f"\nExplanation: {result['explanation']}")


def run_all_scenarios():
    print("="*79)
    print("TASK 2: LOGICAL INFERENCE FOR SERVICE RULES & ADVISORY CONSISTENCY")
    print("="*79)
    
    system = LogicInferenceSystem()
    
    print(f"DEFINED LOGICAL RULES:")
    print("="*79)
    for rule in LOGICAL_RULES[:10]:  # Show first 10 rules
        print(f"\n{rule['id']}: {rule['description']}")
        print(f"   Premises: {', '.join(rule['premises'])}")
        print(f"   Conclusion: {rule['conclusion']}")
        print(f"   Plain English: {rule['plain_english']}")
    
    print(f"\n\n RUNNING TEST SCENARIOS:")
    print("="*79)
    
    results = []
    for scenario in TEST_SCENARIOS:
        result = system.check_scenario_validity(scenario)
        results.append(result)
        print_scenario_result(result, verbose=False)
    
    # Summary
    print("="*79)
    print(f"\n\nSUMMARY:")
    print("="*79)
    valid_count = sum(1 for r in results if r['is_valid'])
    invalid_count = len(results) - valid_count
    
    print(f"Total Scenarios: {len(results)}")
    print(f"Valid Scenarios: {valid_count}")
    print(f"Invalid Scenarios: {invalid_count}")
    
    print(f"\n\nValid Scenarios:")
    for r in results:
        if r['is_valid']:
            print(f"  ✓ {r['scenario_id']}: {r['scenario_name']}")
    
    print(f"\nInvalid Scenarios:")
    for r in results:
        if not r['is_valid']:
            print(f"  ✗ {r['scenario_id']}: {r['scenario_name']}")
            print(f"     Violated: {', '.join(r['violated_rules'])}")


def demonstrate_inference_example():
    """Demonstrate resolution inference with detailed trace"""
    print("\n\n" + "="*79)
    print("DETAILED INFERENCE EXAMPLE")
    print("="*79)
    
    system = LogicInferenceSystem()
    
    # Example: Prove that systems integration leads to service reduction
    facts = [
        "systems_integration_active",
        "platform_conversion_TM",
        "platform_conversion_EXP",
    ]
    
    kb = system.create_kb_from_facts(facts)
    
    query = "service_reduced_airport_corridor"
    
    print(f"\nGiven facts:")
    for fact in facts:
        print(f"  • {fact}: {system.explain_symbol(fact)}")
    
    print(f"\nQuery: Can we prove '{query}'?")
    print(f"Meaning: {system.explain_symbol(query)}")
    
    result, trace = kb.pl_resolution(query)
    
    print(f"\nResolution Result: {result}")
    print(f"\nProof Trace:")
    for step in trace[:10]:  # Show first 10 steps
        print(f"  {step}")
    
    if result:
        print(f"\n✓ Successfully proved: {query}")
    else:
        print(f"\n✗ Could not prove: {query}")


def main():
    """Main function"""
    print("MRT Service Advisory Consistency Checker - Task 2")
    print("Using Resolution-Based Inference")
    
    run_all_scenarios()
    demonstrate_inference_example()



if __name__ == "__main__":
    main()
