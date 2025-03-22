from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional, Union, Dict, Any, Type
from uuid import UUID, uuid4
from abc import ABC, abstractmethod

class FieldType(Enum):
    PLAIN_TEXT = "plain_text"
    EMAIL = "email"
    SINGLE_SELECT = "single_select"
    BOOLEAN = "boolean"
    FILE = "file"

class Operator(Enum):
    EQUALS = "equals"
    NOT_EQUALS = "not_equals"
    CONTAINS = "contains"
    NOT_CONTAINS = "not_contains"
    GREATER_THAN = "greater_than"
    LESS_THAN = "less_than"
    GREATER_THAN_OR_EQUALS = "greater_than_or_equals"
    LESS_THAN_OR_EQUALS = "less_than_or_equals"

class LogicalOperator(Enum):
    AND = "and"
    OR = "or"

@dataclass
class Condition:
    field_id: UUID
    operator: Operator
    value: Any
    logical_operator: Optional[LogicalOperator] = None

@dataclass
class ConditionalLogic:
    conditions: List[Condition]
    logical_operator: LogicalOperator

class BaseField(ABC):
    """Base class for all field types."""
    
    def __init__(
        self,
        id: UUID,
        title: str,
        description: Optional[str],
        required: bool,
        order: int,
        conditional_logic: Optional[ConditionalLogic] = None,
        validation_rules: Optional[Dict[str, Any]] = None
    ):
        self.id = id
        self.title = title
        self.description = description
        self.required = required
        self.order = order
        self.conditional_logic = conditional_logic
        self.validation_rules = validation_rules or {}

    @abstractmethod
    def validate(self, value: Any) -> None:
        """Validate the field value."""
        pass

    @abstractmethod
    def get_field_type(self) -> FieldType:
        """Get the field type."""
        pass

class TextField(BaseField):
    """Plain text field implementation."""
    
    def validate(self, value: Any) -> None:
        if not isinstance(value, str):
            raise ValueError(f"Answer for {self.title} must be a string")
        
        # Apply any additional validation rules
        if "min_length" in self.validation_rules:
            if len(value) < self.validation_rules["min_length"]:
                raise ValueError(f"Answer for {self.title} must be at least {self.validation_rules['min_length']} characters")
        if "max_length" in self.validation_rules:
            if len(value) > self.validation_rules["max_length"]:
                raise ValueError(f"Answer for {self.title} must be at most {self.validation_rules['max_length']} characters")

    def get_field_type(self) -> FieldType:
        return FieldType.PLAIN_TEXT

class EmailField(BaseField):
    """Email field implementation."""
    
    def validate(self, value: Any) -> None:
        if not isinstance(value, str):
            raise ValueError(f"Answer for {self.title} must be a string")
        
        if "@" not in value or "." not in value:
            raise ValueError(f"Answer for {self.title} must be a valid email address")

    def get_field_type(self) -> FieldType:
        return FieldType.EMAIL

class SingleSelectField(BaseField):
    """Single select dropdown field implementation."""
    
    def __init__(
        self,
        id: UUID,
        title: str,
        description: Optional[str],
        required: bool,
        order: int,
        options: List[str],
        conditional_logic: Optional[ConditionalLogic] = None,
        validation_rules: Optional[Dict[str, Any]] = None
    ):
        super().__init__(id, title, description, required, order, conditional_logic, validation_rules)
        self.options = options

    def validate(self, value: Any) -> None:
        if not isinstance(value, str):
            raise ValueError(f"Answer for {self.title} must be a string")
        
        if value not in self.options:
            raise ValueError(f"Answer for {self.title} must be one of the provided options")

    def get_field_type(self) -> FieldType:
        return FieldType.SINGLE_SELECT

class BooleanField(BaseField):
    """Boolean field implementation."""
    
    def validate(self, value: Any) -> None:
        if not isinstance(value, bool):
            raise ValueError(f"Answer for {self.title} must be a boolean")

    def get_field_type(self) -> FieldType:
        return FieldType.BOOLEAN

class FileField(BaseField):
    """File upload field implementation."""
    
    def validate(self, value: Any) -> None:
        if not isinstance(value, dict):
            raise ValueError(f"Answer for {self.title} must be a file object")
        
        if "file_id" not in value:
            raise ValueError(f"Answer for {self.title} must contain a file_id")
        
        if "mime_type" not in value:
            raise ValueError(f"Answer for {self.title} must contain a mime_type")
        
        # Validate file size if specified
        if "max_size" in self.validation_rules:
            if value.get("size", 0) > self.validation_rules["max_size"]:
                raise ValueError(f"File size exceeds maximum allowed size of {self.validation_rules['max_size']} bytes")

    def get_field_type(self) -> FieldType:
        return FieldType.FILE

class FieldFactory:
    """Factory for creating field instances."""
    
    _field_types: Dict[FieldType, Type[BaseField]] = {
        FieldType.PLAIN_TEXT: TextField,
        FieldType.EMAIL: EmailField,
        FieldType.SINGLE_SELECT: SingleSelectField,
        FieldType.BOOLEAN: BooleanField,
        FieldType.FILE: FileField,
    }

    @classmethod
    def create_field(
        cls,
        field_type: FieldType,
        id: UUID,
        title: str,
        description: Optional[str],
        required: bool,
        order: int,
        options: Optional[List[str]] = None,
        conditional_logic: Optional[ConditionalLogic] = None,
        validation_rules: Optional[Dict[str, Any]] = None
    ) -> BaseField:
        """Create a field instance based on the field type."""
        field_class = cls._field_types.get(field_type)
        if not field_class:
            raise ValueError(f"Unknown field type: {field_type}")
        
        if field_type == FieldType.SINGLE_SELECT and not options:
            raise ValueError("Options are required for single select fields")
        
        if field_type == FieldType.SINGLE_SELECT:
            return field_class(
                id=id,
                title=title,
                description=description,
                required=required,
                order=order,
                options=options,
                conditional_logic=conditional_logic,
                validation_rules=validation_rules
            )
        
        return field_class(
            id=id,
            title=title,
            description=description,
            required=required,
            order=order,
            conditional_logic=conditional_logic,
            validation_rules=validation_rules
        )

@dataclass
class Form:
    id: UUID
    title: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime
    fields: List[BaseField] = field(default_factory=list)
    is_active: bool = True
    allow_anonymous: bool = True

    def get_field(self, field_id: UUID) -> Optional[BaseField]:
        """Get a field by its ID."""
        return next((f for f in self.fields if f.id == field_id), None)

    def get_required_fields(self) -> List[BaseField]:
        """Get all required fields."""
        return [f for f in self.fields if f.required]

    def get_visible_fields(self, current_answers: Dict[UUID, Any]) -> List[BaseField]:
        """Get list of fields that should be visible based on current answers."""
        visible_fields = []
        for field in self.fields:
            if not field.conditional_logic:
                visible_fields.append(field)
                continue

            if self._evaluate_conditions(field.conditional_logic, current_answers):
                visible_fields.append(field)

        return visible_fields

    def add_field(self, field: BaseField) -> None:
        """Add a new field to the form."""
        if any(f.id == field.id for f in self.fields):
            raise ValueError(f"Field with id {field.id} already exists")
        
        # Validate field order
        if field.order < 0 or field.order > len(self.fields):
            raise ValueError(f"Invalid field order: {field.order}")
        
        # Ensure order is unique
        if any(f.order == field.order for f in self.fields):
            raise ValueError(f"Field order {field.order} is already taken")
        
        self.fields.append(field)
        self.updated_at = datetime.utcnow()

    def update_field(self, field: BaseField) -> None:
        """Update an existing field."""
        existing_field = next((f for f in self.fields if f.id == field.id), None)
        if not existing_field:
            raise ValueError(f"Field with id {field.id} not found")
        
        # Validate field order if changed
        if existing_field.order != field.order:
            if field.order < 0 or field.order >= len(self.fields):
                raise ValueError(f"Invalid field order: {field.order}")
            if any(f.order == field.order and f.id != field.id for f in self.fields):
                raise ValueError(f"Field order {field.order} is already taken")
        
        # Update field
        index = self.fields.index(existing_field)
        self.fields[index] = field
        self.updated_at = datetime.utcnow()

    def remove_field(self, field_id: UUID) -> None:
        """Remove a field from the form."""
        field = next((f for f in self.fields if f.id == field_id), None)
        if not field:
            raise ValueError(f"Field with id {field_id} not found")
        
        # Check if field is referenced in conditional logic
        for other_field in self.fields:
            if other_field.conditional_logic:
                for condition in other_field.conditional_logic.conditions:
                    if condition.field_id == field_id:
                        raise ValueError(f"Cannot remove field {field_id} as it is referenced in conditional logic")
        
        self.fields.remove(field)
        self.updated_at = datetime.utcnow()

    def add_response(self, response: FormResponse) -> None:
        """Add a new form response."""
        self._validate_response(response)
        self.responses.append(response)

    def _validate_response(self, response: FormResponse) -> None:
        if response.form_id != self.id:
            raise ValueError("Response form_id does not match form id")

        # Validate required fields are answered
        for field in self.fields:
            if field.required and not any(fr.field_id == field.id for fr in response.field_responses):
                raise ValueError(f"Required field {field.title} is not answered")

        # Validate answers match field types
        for field_response in response.field_responses:
            field = next((f for f in self.fields if f.id == field_response.field_id), None)
            if not field:
                raise ValueError(f"Field with id {field_response.field_id} not found in form")

            self._validate_answer_type(field, field_response.value)

    def _validate_answer_type(self, field: BaseField, answer: Any) -> None:
        field.validate(answer)

    def _evaluate_conditions(self, logic: ConditionalLogic, answers: Dict[UUID, Any]) -> bool:
        results = []
        for condition in logic.conditions:
            field_value = answers.get(condition.field_id)
            result = self._evaluate_condition(condition, field_value)
            results.append(result)

        if logic.logical_operator == LogicalOperator.AND:
            return all(results)
        else:  # OR
            return any(results)

    def _evaluate_condition(self, condition: Condition, field_value: Any) -> bool:
        if condition.operator == Operator.EQUALS:
            return field_value == condition.value
        elif condition.operator == Operator.NOT_EQUALS:
            return field_value != condition.value
        elif condition.operator == Operator.CONTAINS:
            return condition.value in field_value
        elif condition.operator == Operator.NOT_CONTAINS:
            return condition.value not in field_value
        elif condition.operator == Operator.GREATER_THAN:
            return field_value > condition.value
        elif condition.operator == Operator.LESS_THAN:
            return field_value < condition.value
        elif condition.operator == Operator.GREATER_THAN_OR_EQUALS:
            return field_value >= condition.value
        elif condition.operator == Operator.LESS_THAN_OR_EQUALS:
            return field_value <= condition.value
        return False

@dataclass
class FieldResponse:
    id: UUID
    field_id: UUID
    value: Any
    submitted_at: datetime
    metadata: Optional[Dict[str, Any]] = None

    def validate(self, field: BaseField) -> None:
        """Validate the response against its field type."""
        field.validate(self.value)

@dataclass
class FormResponse:
    id: UUID
    form_id: UUID
    submitted_at: datetime
    field_responses: List[FieldResponse] = field(default_factory=list)
    respondent_email: Optional[str] = None
    respondent_name: Optional[str] = None

    def add_field_response(self, field_response: FieldResponse) -> None:
        """Add a field response to this form response."""
        if any(fr.id == field_response.id for fr in self.field_responses):
            raise ValueError(f"Field response with id {field_response.id} already exists")
        
        if any(fr.field_id == field_response.field_id for fr in self.field_responses):
            raise ValueError(f"Response for field {field_response.field_id} already exists")
        
        self.field_responses.append(field_response)

    def get_field_response(self, field_id: UUID) -> Optional[FieldResponse]:
        """Get a field response by field ID."""
        return next((fr for fr in self.field_responses if fr.field_id == field_id), None)

    def has_required_fields(self, required_fields: List[BaseField]) -> bool:
        """Check if all required fields have responses."""
        return all(self.get_field_response(field.id) is not None for field in required_fields)

    @property
    def answers(self) -> Dict[UUID, Any]:
        return {fr.field_id: fr.value for fr in self.field_responses}

class FormSubmissionService:
    """Domain service for handling form submissions."""
    
    def submit_response(self, form: Form, response: FormResponse) -> None:
        """
        Submit a form response.
        This service coordinates between Form and FormResponse aggregates.
        """
        if not form.is_active:
            raise ValueError("Form is not active")

        # Validate form ID matches
        if response.form_id != form.id:
            raise ValueError("Response form_id does not match form id")

        # Validate all required fields are answered
        required_fields = form.get_required_fields()
        if not response.has_required_fields(required_fields):
            missing_fields = [f.title for f in required_fields if not response.get_field_response(f.id)]
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

        # Validate each field response
        for field_response in response.field_responses:
            field = form.get_field(field_response.field_id)
            if not field:
                raise ValueError(f"Field with id {field_response.field_id} not found in form")
            
            field_response.validate(field)

        # Validate conditional logic
        visible_fields = form.get_visible_fields(response.answers)
        for field_response in response.field_responses:
            field = form.get_field(field_response.field_id)
            if field and field not in visible_fields:
                raise ValueError(f"Field {field.title} is not visible based on current answers") 