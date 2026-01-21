"""
Data validation and quality checking utilities for scraped data.
"""
import logging
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime

from .config import QUALITY_THRESHOLDS, CRITICAL_FIELDS

logger = logging.getLogger(__name__)


class DataValidator:
    """
    Validates scraped data for quality and completeness.
    """
    
    @staticmethod
    def validate_university(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Validate university data.
        
        Returns:
            (is_valid, list_of_errors)
        """
        errors = []
        
        # Check critical fields
        for field in CRITICAL_FIELDS['university']:
            if field not in data or not data[field]:
                errors.append(f"Missing critical field: {field}")
        
        # Validate data types and formats
        if 'website' in data and data['website']:
            if not data['website'].startswith('http'):
                errors.append(f"Invalid website URL: {data['website']}")
        
        if 'tuition_annual_ron' in data and data['tuition_annual_ron']:
            try:
                tuition = int(data['tuition_annual_ron'])
                if tuition < 0 or tuition > 50000:  # Sanity check
                    errors.append(f"Tuition RON out of range: {tuition}")
            except (ValueError, TypeError):
                errors.append(f"Invalid tuition_annual_ron: {data['tuition_annual_ron']}")
        
        if 'tuition_annual_eur' in data and data['tuition_annual_eur']:
            try:
                tuition = int(data['tuition_annual_eur'])
                if tuition < 0 or tuition > 15000:  # Sanity check
                    errors.append(f"Tuition EUR out of range: {tuition}")
            except (ValueError, TypeError):
                errors.append(f"Invalid tuition_annual_eur: {data['tuition_annual_eur']}")
        
        if 'acceptance_rate' in data and data['acceptance_rate'] is not None:
            try:
                rate = float(data['acceptance_rate'])
                if rate < 0 or rate > 1:
                    errors.append(f"Acceptance rate must be 0-1: {rate}")
            except (ValueError, TypeError):
                errors.append(f"Invalid acceptance_rate: {data['acceptance_rate']}")
        
        if 'avg_bac_score' in data and data['avg_bac_score'] is not None:
            try:
                score = float(data['avg_bac_score'])
                if score < 5 or score > 10:  # Romanian scale is 1-10, but realistic is 5-10
                    errors.append(f"Bac score out of range: {score}")
            except (ValueError, TypeError):
                errors.append(f"Invalid avg_bac_score: {data['avg_bac_score']}")
        
        if 'student_count' in data and data['student_count'] is not None:
            try:
                count = int(data['student_count'])
                if count < 0 or count > 100000:  # Sanity check
                    errors.append(f"Student count out of range: {count}")
            except (ValueError, TypeError):
                errors.append(f"Invalid student_count: {data['student_count']}")
        
        if 'type' in data and data['type']:
            if data['type'] not in ['public', 'private']:
                errors.append(f"Invalid type: {data['type']}")
        
        # Check data completeness
        filled_fields = sum(1 for v in data.values() if v is not None and v != '')
        if filled_fields < QUALITY_THRESHOLDS['min_university_fields']:
            errors.append(f"Too few filled fields: {filled_fields}")
        
        is_valid = len(errors) == 0
        
        return is_valid, errors
    
    @staticmethod
    def validate_program(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Validate program data.
        
        Returns:
            (is_valid, list_of_errors)
        """
        errors = []
        
        # Check critical fields
        for field in CRITICAL_FIELDS['program']:
            if field not in data or not data[field]:
                errors.append(f"Missing critical field: {field}")
        
        # Validate field enum
        if 'field' in data and data['field']:
            valid_fields = [
                'stem', 'engineering', 'business', 'health',
                'arts_humanities', 'social_sciences', 'law', 'education', 'other'
            ]
            if data['field'] not in valid_fields:
                errors.append(f"Invalid field: {data['field']}")
        
        # Validate degree_level enum
        if 'degree_level' in data and data['degree_level']:
            valid_levels = ['bachelor', 'master', 'phd']
            if data['degree_level'] not in valid_levels:
                errors.append(f"Invalid degree_level: {data['degree_level']}")
        
        # Validate duration
        if 'duration_years' in data and data['duration_years'] is not None:
            try:
                duration = int(data['duration_years'])
                if duration < 1 or duration > 8:  # Most programs are 1-8 years
                    errors.append(f"Duration out of range: {duration}")
            except (ValueError, TypeError):
                errors.append(f"Invalid duration_years: {data['duration_years']}")
        
        # Validate min_bac_score
        if 'min_bac_score' in data and data['min_bac_score'] is not None:
            try:
                score = float(data['min_bac_score'])
                if score < 5 or score > 10:
                    errors.append(f"Min bac score out of range: {score}")
            except (ValueError, TypeError):
                errors.append(f"Invalid min_bac_score: {data['min_bac_score']}")
        
        # Check data completeness
        filled_fields = sum(1 for v in data.values() if v is not None and v != '')
        if filled_fields < QUALITY_THRESHOLDS['min_program_fields']:
            errors.append(f"Too few filled fields: {filled_fields}")
        
        is_valid = len(errors) == 0
        
        return is_valid, errors
    
    @staticmethod
    def validate_course(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Validate course data.
        
        Returns:
            (is_valid, list_of_errors)
        """
        errors = []
        
        # Check critical fields
        for field in CRITICAL_FIELDS['course']:
            if field not in data or not data[field]:
                errors.append(f"Missing critical field: {field}")
        
        # Validate name length
        if 'name' in data and data['name']:
            if len(data['name']) < 3:
                errors.append(f"Course name too short: {data['name']}")
            if len(data['name']) > 300:
                errors.append(f"Course name too long: {data['name']}")
        
        # Validate year of study
        if 'year_of_study' in data and data['year_of_study'] is not None:
            try:
                year = int(data['year_of_study'])
                if year < 1 or year > 8:
                    errors.append(f"Year of study out of range: {year}")
            except (ValueError, TypeError):
                errors.append(f"Invalid year_of_study: {data['year_of_study']}")
        
        is_valid = len(errors) == 0
        
        return is_valid, errors


class DataQualityChecker:
    """
    Checks overall data quality and generates reports.
    """
    
    @staticmethod
    def check_universities(universities: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Check quality of university data list.
        
        Returns:
            Quality report with statistics and issues
        """
        total = len(universities)
        valid = 0
        invalid = 0
        all_errors = []
        
        field_completeness = {}
        
        for uni in universities:
            is_valid, errors = DataValidator.validate_university(uni)
            
            if is_valid:
                valid += 1
            else:
                invalid += 1
                all_errors.extend(errors)
            
            # Track field completeness
            for key, value in uni.items():
                if key not in field_completeness:
                    field_completeness[key] = {'filled': 0, 'total': 0}
                
                field_completeness[key]['total'] += 1
                if value is not None and value != '':
                    field_completeness[key]['filled'] += 1
        
        # Calculate completeness percentages
        for field, stats in field_completeness.items():
            stats['percentage'] = (stats['filled'] / stats['total'] * 100) if stats['total'] > 0 else 0
        
        report = {
            'total_universities': total,
            'valid': valid,
            'invalid': invalid,
            'validity_rate': (valid / total * 100) if total > 0 else 0,
            'field_completeness': field_completeness,
            'common_errors': DataQualityChecker._count_error_types(all_errors),
            'timestamp': datetime.now().isoformat()
        }
        
        return report
    
    @staticmethod
    def check_programs(programs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Check quality of program data list.
        
        Returns:
            Quality report with statistics and issues
        """
        total = len(programs)
        valid = 0
        invalid = 0
        all_errors = []
        
        field_completeness = {}
        field_distribution = {}
        
        for prog in programs:
            is_valid, errors = DataValidator.validate_program(prog)
            
            if is_valid:
                valid += 1
            else:
                invalid += 1
                all_errors.extend(errors)
            
            # Track field completeness
            for key, value in prog.items():
                if key not in field_completeness:
                    field_completeness[key] = {'filled': 0, 'total': 0}
                
                field_completeness[key]['total'] += 1
                if value is not None and value != '':
                    field_completeness[key]['filled'] += 1
            
            # Track field distribution
            if 'field' in prog and prog['field']:
                field = prog['field']
                field_distribution[field] = field_distribution.get(field, 0) + 1
        
        # Calculate completeness percentages
        for field, stats in field_completeness.items():
            stats['percentage'] = (stats['filled'] / stats['total'] * 100) if stats['total'] > 0 else 0
        
        report = {
            'total_programs': total,
            'valid': valid,
            'invalid': invalid,
            'validity_rate': (valid / total * 100) if total > 0 else 0,
            'field_completeness': field_completeness,
            'field_distribution': field_distribution,
            'common_errors': DataQualityChecker._count_error_types(all_errors),
            'timestamp': datetime.now().isoformat()
        }
        
        return report
    
    @staticmethod
    def check_courses(courses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Check quality of course data list.
        
        Returns:
            Quality report with statistics and issues
        """
        total = len(courses)
        valid = 0
        invalid = 0
        all_errors = []
        
        for course in courses:
            is_valid, errors = DataValidator.validate_course(course)
            
            if is_valid:
                valid += 1
            else:
                invalid += 1
                all_errors.extend(errors)
        
        report = {
            'total_courses': total,
            'valid': valid,
            'invalid': invalid,
            'validity_rate': (valid / total * 100) if total > 0 else 0,
            'common_errors': DataQualityChecker._count_error_types(all_errors),
            'timestamp': datetime.now().isoformat()
        }
        
        return report
    
    @staticmethod
    def _count_error_types(errors: List[str]) -> Dict[str, int]:
        """Count occurrences of each error type."""
        error_counts = {}
        
        for error in errors:
            # Normalize error message (remove specific values)
            error_type = error.split(':')[0]
            error_counts[error_type] = error_counts.get(error_type, 0) + 1
        
        # Sort by frequency
        sorted_errors = sorted(error_counts.items(), key=lambda x: x[1], reverse=True)
        
        return dict(sorted_errors[:10])  # Top 10 errors
