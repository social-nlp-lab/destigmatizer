import sys
import os
import json
import argparse
import pytest


# Import test modules correctly
from reframe.tests import (
    test_drug_classifier,
    test_stigma_classifier, 
    test_text_analyzer,
    test_rewriter,
    test_emotion_detector
)

def run_all_tests(api_key=None, model=None, client_type=None):
    """
    Run all tests in sequence.
    
    Args:
        api_key (str, optional): API key for the LLM service
        model (str, optional): Model name to use for testing
        client_type (str, optional): Type of client ("openai", "together", "claude", etc.)
    """
    print("=" * 80)
    print("RUNNING ALL REFRAME TESTS")
    print(f"Model: {model or 'default'}")
    print(f"Client type: {client_type}")
    print("=" * 80)
    
    print("\n1. Drug Classification Test")
    print("-" * 40)
    test_drug_classifier(api_key, model, client_type)
    
    print("\n2. Stigma Classification Test")
    print("-" * 40)
    test_stigma_classifier(api_key, model, client_type)
    
    print("\n3. Text Analysis Test")
    print("-" * 40)
    test_text_analyzer(api_key, model, client_type)
    
    print("\n4. Text Rewriting Test")
    print("-" * 40)
    test_rewriter(api_key, model, client_type)
    
    print("\n5. Emotion Detection Test")
    print("-" * 40)
    test_emotion_detector(api_key, model, client_type)
    
    print("\n" + "=" * 80)
    print("ALL TESTS COMPLETED")
    print("=" * 80)

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Run reframe tests')
    parser.add_argument('--api_key', help='API key for LLM service')
    parser.add_argument('--model', help='Model name to use for testing')
    parser.add_argument('--client', default='openai',
                      help='Client type (e.g., openai, together, claude)')
    parser.add_argument('--pytest', action='store_true', help='Run tests using pytest')
    parser.add_argument('test', nargs='?', choices=['all', 'drug', 'stigma', 'analysis', 'rewriter', 'emotion'], 
                       default='all', help='Specific test to run')
    
    args = parser.parse_args()
    
    # Get API key either from parameter, environment variables, or secrets file
    api_key = args.api_key
    if api_key is None:
        # First try to get from environment variables
        if args.client_type.lower() == "openai":
            api_key = os.environ.get("OPENAI_API_KEY")
        elif args.client_type.lower() == "together":
            api_key = os.environ.get("TOGETHER_API_KEY")
        elif args.client_type.lower() == "claude":
            api_key = os.environ.get("ANTHROPIC_API_KEY")
        
        # If not found in env vars, try secrets file
        if api_key is None:
            try:
                with open("secrets.json") as f:
                    secrets = json.load(f)
                    if args.client_type.lower() == "openai":
                        api_key = secrets.get("OPENAI_API_KEY")
                    elif args.client_type.lower() == "together":
                        api_key = secrets.get("TOGETHER_API_KEY")
                    elif args.client_type.lower() == "claude":
                        api_key = secrets.get("ANTHROPIC_API_KEY")
            except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
                print(f"Error loading API key from secrets.json: {e}")
                print("Please provide an API key using --api_key or set the appropriate environment variable")
                sys.exit(1)
                
        if api_key is None:
            print(f"No API key found for {args.client_type}. Please provide an API key.")
            sys.exit(1)
    
    # If pytest flag is used, run with pytest
    if args.pytest:
        pytest_args = []
        if args.test != 'all':
            pytest_args.append(f"test_{args.test}_*.py")
        # Pass API key and model as environment variables
        os.environ["REFRAME_API_KEY"] = api_key
        os.environ["REFRAME_MODEL"] = args.model or ""
        os.environ["REFRAME_CLIENT_TYPE"] = args.client_type
        pytest.main(pytest_args)
        return
        
    # Otherwise run in script mode
    if args.test == 'all':
        run_all_tests(api_key=api_key, model=args.model, client_type=args.client_type)
    elif args.test == 'drug':
        test_drug_classifier.test_drug_classifier(api_key, args.model, args.client_type)
    elif args.test == 'stigma':
        test_stigma_classifier.test_stigma_classifier(api_key, args.model, args.client_type)
    elif args.test == 'analysis':
        test_text_analyzer.test_text_analyzer(api_key, args.model, args.client_type)
    elif args.test == 'rewriter':
        test_rewriter.test_rewriter(api_key, args.model, args.client_type)
    elif args.test == 'emotion':
        test_emotion_detector.test_emotion_detector(api_key, args.model, args.client_type)

if __name__ == "__main__":
    main()