import argparse
import redactor


if __name__ == "__main__":
    

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--input",type = str, required = True, help = "Input files path", nargs = "*", action = "append" )
    arg_parser.add_argument("--names", required = False, help = "Redacts names in input files", action = "store_true")
    arg_parser.add_argument("--dates", required = False, help = "Redacts dates in input files", action = "store_true")
    arg_parser.add_argument("--phones", required = False, help = "Redacts phone numbers in input files", action = "store_true")
    arg_parser.add_argument("--genders", required = False, help = "Redacts genders in input files", action = "store_true")
    arg_parser.add_argument("--concept", type = str, required = False, help = "Redacts concept word in input files", action = "append")
    arg_parser.add_argument("--stats", type = str, required = False, help = "Gives statistics for redacted files")
    arg_parser.add_argument("--output", type = str, required = True, help = "output folder or file path")

    args = arg_parser.parse_args()
    input_data = redactor.handle_input_files(args.input)

    
    if args.names:
        input_data = redactor.redact_names(input_data)
    
    if args.dates:
        input_data = redactor.redact_dates(input_data)
    
    if args.phones:
        input_data = redactor.redact_phones(input_data)
        

    if args.genders:
        input_data = redactor.redact_gender(input_data)

    if args.concept:
        input_data = redactor.redact_concept(input_data, args.concept)
        
    if args.output:
        redactor.get_output(args.input, input_data, args.output)

    if args.stats:
        
        redactor.write_stats()

    
