import os
import sys

from exceptions import FileProcessingError
from file_reader import read_csv_file
from validator import validate_all_records
from transformer import calculate_totals, aggregate_by_store, aggregate_by_product
from report_writer import write_summary_report, write_clean_csv, write_error_log

def process_sales_file(input_path, output_dir):
    """
    Main processing pipeline.
    
    1. Read the input file
    2. Validate all records
    3. Transform valid records
    4. Generate reports
    5. Handle any errors gracefully
    
    Returns: ProcessingResult with statistics
    """
    #Make directory and files for records and reports
    os.makedirs(output_dir, exist_ok=True)

    summary_report_path = os.path.join(output_dir, "summary_report.txt")
    clean_csv_path = os.path.join(output_dir, "clean_data.csv")
    error_log_path = os.path.join(output_dir, "error_log.txt")

    try:
        #Step 1: read the input file
        raw_records = read_csv_file(input_path)
        #Step 2: validate all records
        valid_records, errors = validate_all_records(raw_records)
        #Step 3: transform valid records
        valid_with_totals = calculate_totals(valid_records)
        aggregations = {
            "sales_by_store": aggregate_by_store(valid_with_totals),
            "qty_by_product": aggregate_by_product(valid_with_totals)
        }
        #Step 4: generate reports
        write_summary_report(summary_report_path, valid_with_totals, errors, aggregations)
        write_clean_csv(clean_csv_path, valid_with_totals)
        write_error_log(error_log_path, errors)

        return{
            "input_path": input_path,
            "output_dir": output_dir,
            "total_records": len(raw_records),
            "valid_records": len(valid_with_totals),
            "error_records": len(errors),
            "summary_report_path": summary_report_path,
            "clean_csv_path": clean_csv_path,
            "error_log_path": error_log_path,
        }
        #Step 5: handle any errors gracefully
    except FileProcessingError as e:
        fatal_errors = [f"Fatal error: {e}"]
        aggregations = {"sales_by_store": {}, "qty_by_product": {}}

        write_summary_report(summary_report_path, [], fatal_errors, aggregations)
        write_clean_csv(clean_csv_path, [])
        write_error_log(error_log_path, fatal_errors)

        return {
            "input_path": input_path,
            "output_dir": output_dir,
            "total_records": 0,
            "valid_records": 0,
            "error_records": len(fatal_errors),
            "summary_report_path": summary_report_path,
            "clean_csv_path": clean_csv_path,
            "error_log_path": error_log_path,
        }
    except Exception as e:
        fatal_errors = [f"Unexpected error: {e}"]
        aggregations = {"sales_by_store": {}, "qty_by_product": {}}

        write_summary_report(summary_report_path, [], fatal_errors, aggregations)
        write_clean_csv(clean_csv_path, [])
        write_error_log(error_log_path, fatal_errors)

        return {
            "input_path": input_path,
            "output_dir": output_dir,
            "total_records": 0,
            "valid_records": 0,
            "error_records": len(fatal_errors),
            "summary_report_path": summary_report_path,
            "clean_csv_path": clean_csv_path,
            "error_log_path": error_log_path,
        }



if __name__ == "__main__":
    # Process from command line
    if len(sys.argv) < 2:
        print("Usage: python processor.py <input_csv_path> [output_dir]")
        sys.exit(1)
    input_path = sys.argv[1]
    out_dir = sys.argv[2] if len(sys.argv) >= 3 else "output"
    result = process_sales_file(input_path, out_dir)

    print("Processing complete. Summary:")
    print(f"-Input file: {result['input_path']}")
    print(f"-Output directory: {result['output_dir']}")
    print(f"-Total records: {result['total_records']}")
    print(f"-Valid records: {result['valid_records']}")
    print(f"-Error records: {result['error_records']}")
    print(f"Summary report: {result['summary_report_path']}")
    print(f"-Clean CSV: {result['clean_csv_path']}")
    print(f"-Error log: {result['error_log_path']}")