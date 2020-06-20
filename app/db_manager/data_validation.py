def validate_documents_dataset(dataset):
    """Validates if documents dataset has correct columns, data format etc."""
    errors = []

    required_columns = {'book', 'chapter', 'verse', 'text'}

    dataset_columns = set(dataset.columns.values)
    if len(dataset_columns) != 4:
        error_column = f"Dataset should have 4 columns"
        errors.append(error_column)
        return errors

    col_difference = dataset_columns - required_columns
    col_difference = ', '.join(col_difference)
    if len(col_difference) > 0:
        error_column = f"Invalid columns in dataset: {col_difference}"
        errors.append(error_column)
        return errors

    return errors


def documents_dataset_check(dataset):
    """Compile validations before dataset upload for documents"""

    validation_errors = validate_documents_dataset(dataset)

    return validation_errors
