import streamlit as st
import pandas as pd
import numpy as np

from numpy.random import default_rng
from faker import Faker
from array import array
from datetime import datetime


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="ETL Automation Labs - Customer Data Generator",
    page_icon="🧪",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 38px;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0px;
    }

    .sub-title {
        font-size: 18px;
        text-align: center;
        margin-bottom: 25px;
    }

    .banner {
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        font-size: 32px;
        font-weight: bold;
        letter-spacing: 2px;
        margin-bottom: 25px;
        border: 2px solid #444;
    }

    .metric-box {
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #ddd;
        text-align: center;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="banner">ETL AUTOMATION LABS</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="main-title">Customer Test Data Generator</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">'
    'Data Quality & ETL Testing Synthetic Data Generator'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# INITIALIZE FAKER
# ============================================================

fake = Faker("en_IN")


# ============================================================
# COLUMN DEFINITIONS
# ============================================================

CUSTOMER_COLUMNS = {
    "customer_id": "this is customer number increment by 1",
    "first_name": "First Name",
    "last_name": "Last Name",
    "full_name": "Full Name",
    "gender": "Gender",
    "date_of_birth": "Date of Birth",
    "email": "Email",
    "phone": "Phone",
    "address": "Address",
    "city": "City",
    "state": "State",
    "country": "Country",
    "postal_code": "Postal Code",
    "customer_type": "Customer Type",
    "registration_date": "Registration Date",
    "status": "Status",
    "income": "Income",
    "credit_score": "Credit Score",
    "created_timestamp": "Created Timestamp"
}


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("⚙️ Generator Configuration")

row_count = st.sidebar.number_input(
    "Number of Rows",
    min_value=1,
    max_value=1000000,
    value=1,
    step=10
)


# ============================================================
# COLUMN SELECTION
# ============================================================

st.sidebar.subheader("📋 Select Customer Columns")

selected_columns = st.sidebar.multiselect(
    "Columns",
    options=list(CUSTOMER_COLUMNS.keys()),
    default=[
        "customer_id",
        "first_name",
        "last_name",
        "full_name",
        "gender",
        "email",
        "phone",
        "date_of_birth",
        "city",
        "state",
        "country",
        "postal_code",
        "customer_type",
        "registration_date",
        "status"
    ],
    format_func=lambda x: CUSTOMER_COLUMNS[x]
)


# ============================================================
# TEST DATA SCENARIOS
# ============================================================

st.sidebar.subheader("🧪 Data Quality Scenarios")

scenario_options = [
    "Positive",
    "Duplicate",
    "Null",
    "Invalid",
    "Boundary"
]

selected_scenarios = st.sidebar.multiselect(
    "Select scenarios",
    scenario_options,
    default=["Positive"]
)


# ============================================================
# SCENARIO PERCENTAGES
# ============================================================

st.sidebar.subheader("📊 Scenario Distribution")

scenario_percentages = {}

if selected_scenarios:

    default_percentage = round(
        100 / len(selected_scenarios),
        2
    )

    for scenario in selected_scenarios:

        scenario_percentages[scenario] = st.sidebar.number_input(
            f"{scenario} %",
            min_value=0.0,
            max_value=100.0,
            value=default_percentage,
            step=1.0,
            key=f"percentage_{scenario}"
        )

    total_percentage = sum(
        scenario_percentages.values()
    )

    st.sidebar.write(
        f"**Total: {total_percentage:.2f}%**"
    )

else:

    total_percentage = 0


# ============================================================
# RANDOM SEED
# ============================================================

random_seed = st.sidebar.number_input(
    "Random Seed",
    min_value=1,
    max_value=999999,
    value=12345
)


# ============================================================
# ADVANCED OPTIONS
# ============================================================

st.sidebar.subheader("⚡ Advanced Options")

preview_rows = st.sidebar.number_input(
    "Preview Rows",
    min_value=5,
    max_value=1000,
    value=20
)

include_scenario_column = st.sidebar.checkbox(
    "Include DQ Scenario Column",
    value=True
)


# ============================================================
# VALIDATE INPUT
# ============================================================

def validate_configuration():

    if not selected_columns:
        st.error("Please select at least one column.")
        return False

    if not selected_scenarios:
        st.error("Please select at least one DQ scenario.")
        return False

    total = sum(scenario_percentages.values())

    if abs(total - 100) > 0.01:
        st.error(
            f"Scenario percentages must total 100%. Current total = {total:.2f}%"
        )
        return False

    if "customer_id" not in selected_columns:
        st.warning(
            "Customer ID is not selected. Duplicate testing may be limited."
        )

    return True


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def generate_customer_ids(count):

    """
    Uses Python array for efficient numeric storage.
    """

    numbers = array(
        "Q",
        range(1, count + 1)
    )

    return np.array(
        [f"CUST{x:09d}" for x in numbers],
        dtype=object
    )


def generate_names(count):

    first_names = np.array(
        [fake.first_name() for _ in range(count)],
        dtype=object
    )

    last_names = np.array(
        [fake.last_name() for _ in range(count)],
        dtype=object
    )

    full_names = np.char.add(
        np.char.add(first_names.astype(str), " "),
        last_names.astype(str)
    )

    return first_names, last_names, full_names


def generate_gender(rng, count):

    return rng.choice(
        ["Male", "Female", "Other"],
        size=count,
        p=[0.48, 0.48, 0.04]
    )


def generate_emails(first_names, last_names):

    result = []

    for first, last in zip(first_names, last_names):

        result.append(
            f"{first.lower()}.{last.lower()}"
            f"{rng_global.integers(1, 9999)}"
            "@gmail.com"
        )

    return np.array(result, dtype=object)


def generate_phone_numbers(rng, count):

    numbers = rng.integers(
        6000000000,
        9999999999,
        size=count
    )

    return np.array(
        [f"+91{x}" for x in numbers],
        dtype=object
    )


def generate_dates(rng, count):

    start = np.datetime64("1960-01-01")
    end = np.datetime64("2005-12-31")

    days = (
        end - start
    ).astype("timedelta64[D]").astype(int)

    random_days = rng.integers(
        0,
        days,
        size=count
    )

    dates = (
        start +
        random_days.astype("timedelta64[D]")
    )

    return dates.astype(str)


def generate_registration_dates(rng, count):

    start = np.datetime64("2020-01-01")
    end = np.datetime64("2026-12-31")

    days = (
        end - start
    ).astype("timedelta64[D]").astype(int)

    random_days = rng.integers(
        0,
        days,
        size=count
    )

    dates = (
        start +
        random_days.astype("timedelta64[D]")
    )

    return dates.astype(str)


def generate_income(rng, count):

    return np.round(
        rng.uniform(
            15000,
            500000,
            size=count
        ),
        2
    )


def generate_credit_score(rng, count):

    return rng.integers(
        300,
        851,
        size=count
    )


def generate_postal_codes(rng, count):

    return np.array(
        [
            f"{x:06d}"
            for x in rng.integers(
                100000,
                999999,
                size=count
            )
        ],
        dtype=object
    )


def generate_customer_types(rng, count):

    return rng.choice(
        [
            "Regular",
            "Premium",
            "VIP",
            "Corporate"
        ],
        size=count,
        p=[
            0.55,
            0.25,
            0.10,
            0.10
        ]
    )


def generate_status(rng, count):

    return rng.choice(
        [
            "Active",
            "Inactive",
            "Blocked",
            "Pending"
        ],
        size=count,
        p=[
            0.70,
            0.15,
            0.05,
            0.10
        ]
    )


def generate_addresses(count):

    return np.array(
        [
            fake.street_address()
            for _ in range(count)
        ],
        dtype=object
    )


def generate_cities(count):

    return np.array(
        [
            fake.city()
            for _ in range(count)
        ],
        dtype=object
    )


def generate_states(count):

    states = np.array(
        [
            "Karnataka",
            "Andhra Pradesh",
            "Telangana",
            "Tamil Nadu",
            "Kerala",
            "Maharashtra",
            "Delhi",
            "Gujarat",
            "Rajasthan",
            "West Bengal"
        ]
    )

    return rng_global.choice(
        states,
        size=count
    )


def generate_customer_data(
    count,
    columns,
    scenarios,
    percentages,
    seed
):

    global rng_global

    rng_global = default_rng(seed)

    # --------------------------------------------------------
    # Create base positive dataset
    # --------------------------------------------------------

    data = {}

    customer_ids = generate_customer_ids(count)

    first_names, last_names, full_names = generate_names(count)

    gender = generate_gender(
        rng_global,
        count
    )

    emails = np.array(
        [
            f"{first.lower()}.{last.lower()}"
            f"{rng_global.integers(1, 999999)}"
            "@gmail.com"
            for first, last
            in zip(first_names, last_names)
        ],
        dtype=object
    )

    phones = generate_phone_numbers(
        rng_global,
        count
    )

    dob = generate_dates(
        rng_global,
        count
    )

    registration_dates = generate_registration_dates(
        rng_global,
        count
    )

    incomes = generate_income(
        rng_global,
        count
    )

    credit_scores = generate_credit_score(
        rng_global,
        count
    )

    postal_codes = generate_postal_codes(
        rng_global,
        count
    )

    customer_types = generate_customer_types(
        rng_global,
        count
    )

    statuses = generate_status(
        rng_global,
        count
    )

    addresses = generate_addresses(count)

    cities = generate_cities(count)

    states = generate_states(count)

    countries = np.full(
        count,
        "India",
        dtype=object
    )

    created_timestamp = np.full(
        count,
        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        dtype=object
    )

    # --------------------------------------------------------
    # Build dataset
    # --------------------------------------------------------

    all_data = {

        "customer_id": customer_ids,

        "first_name": first_names,

        "last_name": last_names,

        "full_name": full_names,

        "gender": gender,

        "date_of_birth": dob,

        "email": emails,

        "phone": phones,

        "address": addresses,

        "city": cities,

        "state": states,

        "country": countries,

        "postal_code": postal_codes,

        "customer_type": customer_types,

        "registration_date": registration_dates,

        "status": statuses,

        "income": incomes,

        "credit_score": credit_scores,

        "created_timestamp": created_timestamp
    }

    for column in columns:

        data[column] = all_data[column]

    df = pd.DataFrame(data)

    # --------------------------------------------------------
    # Create scenario assignment
    # --------------------------------------------------------

    scenario_names = list(percentages.keys())

    probability = np.array(
        [
            percentages[x] / 100
            for x in scenario_names
        ]
    )

    scenario_assignment = rng_global.choice(
        scenario_names,
        size=count,
        p=probability
    )

    # --------------------------------------------------------
    # Apply scenarios
    # --------------------------------------------------------

    for scenario in scenario_names:

        indexes = np.where(
            scenario_assignment == scenario
        )[0]

        if len(indexes) == 0:
            continue

        # ====================================================
        # DUPLICATE
        # ====================================================

        if scenario == "Duplicate":

            if len(df) > 1:

                source_indexes = rng_global.choice(
                    np.arange(len(df)),
                    size=len(indexes),
                    replace=True
                )

                for target_index, source_index in zip(
                    indexes,
                    source_indexes
                ):

                    df.iloc[target_index] = (
                        df.iloc[source_index].values
                    )

        # ====================================================
        # NULL
        # ====================================================

        elif scenario == "Null":

            nullable_columns = [
                c for c in columns
                if c != "customer_id"
            ]

            if nullable_columns:

                for index in indexes:

                    column = rng_global.choice(
                        nullable_columns
                    )

                    df.at[
                        index,
                        column
                    ] = None

        # ====================================================
        # INVALID
        # ====================================================

        elif scenario == "Invalid":

            for index in indexes:

                invalid_column = rng_global.choice(
                    columns
                )

                if invalid_column == "email":

                    df.at[
                        index,
                        invalid_column
                    ] = "invalid_email"

                elif invalid_column == "phone":

                    df.at[
                        index,
                        invalid_column
                    ] = "ABC123XYZ"

                elif invalid_column == "gender":

                    df.at[
                        index,
                        invalid_column
                    ] = "UNKNOWN_VALUE"

                elif invalid_column == "postal_code":

                    df.at[
                        index,
                        invalid_column
                    ] = "INVALID"

                elif invalid_column == "credit_score":

                    df.at[
                        index,
                        invalid_column
                    ] = 9999

                elif invalid_column == "income":

                    df.at[
                        index,
                        invalid_column
                    ] = -999999

                elif invalid_column == "status":

                    df.at[
                        index,
                        invalid_column
                    ] = "INVALID_STATUS"

                else:

                    df.at[
                        index,
                        invalid_column
                    ] = "@@@INVALID@@@"

        # ====================================================
        # BOUNDARY
        # ====================================================

        elif scenario == "Boundary":

            for index in indexes:

                boundary_column = rng_global.choice(
                    columns
                )

                if boundary_column == "income":

                    df.at[
                        index,
                        boundary_column
                    ] = 0

                elif boundary_column == "credit_score":

                    df.at[
                        index,
                        boundary_column
                    ] = rng_global.choice(
                        [300, 301, 849, 850]
                    )

                elif boundary_column == "first_name":

                    df.at[
                        index,
                        boundary_column
                    ] = ""

                elif boundary_column == "last_name":

                    df.at[
                        index,
                        boundary_column
                    ] = ""

                elif boundary_column == "email":

                    df.at[
                        index,
                        boundary_column
                    ] = "a@b.co"

                elif boundary_column == "phone":

                    df.at[
                        index,
                        boundary_column
                    ] = "+910000000000"

                elif boundary_column == "postal_code":

                    df.at[
                        index,
                        boundary_column
                    ] = "000000"

                else:

                    df.at[
                        index,
                        boundary_column
                    ] = ""

    # --------------------------------------------------------
    # Add scenario column
    # --------------------------------------------------------

    if include_scenario_column:

        df["dq_scenario"] = scenario_assignment

    return df


# ============================================================
# GENERATE BUTTON
# ============================================================

generate_button = st.sidebar.button(
    "🚀 Generate Customer Data",
    type="primary",
    use_container_width=True
)


# ============================================================
# MAIN APPLICATION
# ============================================================

if generate_button:

    if not validate_configuration():

        st.stop()

    progress = st.progress(0)

    status_text = st.empty()

    status_text.info(
        "Generating customer test data..."
    )

    progress.progress(20)

    try:

        start_time = datetime.now()

        df = generate_customer_data(
            count=row_count,
            columns=selected_columns,
            scenarios=selected_scenarios,
            percentages=scenario_percentages,
            seed=random_seed
        )

        progress.progress(80)

        end_time = datetime.now()

        execution_time = (
            end_time - start_time
        ).total_seconds()

        progress.progress(100)

        status_text.success(
            f"Data generated successfully in "
            f"{execution_time:.2f} seconds."
        )

        # Store dataframe in session state

        st.session_state["customer_df"] = df

        st.session_state["generation_time"] = execution_time

    except Exception as e:

        st.error(
            f"Data generation failed: {str(e)}"
        )


# ============================================================
# DISPLAY GENERATED DATA
# ============================================================

if "customer_df" in st.session_state:

    df = st.session_state["customer_df"]

    execution_time = st.session_state[
        "generation_time"
    ]

    st.divider()

    st.subheader("📊 Generation Summary")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Total Records",
            f"{len(df):,}"
        )

    with col2:

        st.metric(
            "Total Columns",
            len(df.columns)
        )

    with col3:

        st.metric(
            "Generation Time",
            f"{execution_time:.2f}s"
        )

    with col4:

        st.metric(
            "Memory",
            f"{df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB"
        )

    # ========================================================
    # DATA PREVIEW
    # ========================================================

    st.subheader(
        f"🔍 Data Preview - First {preview_rows} Rows"
    )

    st.dataframe(
        df.head(preview_rows),
        use_container_width=True,
        height=450
    )

    # ========================================================
    # DQ SUMMARY
    # ========================================================

    if "dq_scenario" in df.columns:

        st.subheader("🧪 Data Quality Scenario Summary")

        scenario_summary = (
            df["dq_scenario"]
            .value_counts()
            .reset_index()
        )

        scenario_summary.columns = [
            "Scenario",
            "Record Count"
        ]

        scenario_summary["Percentage"] = (
            scenario_summary["Record Count"]
            / len(df)
            * 100
        ).round(2)

        st.dataframe(
            scenario_summary,
            use_container_width=True,
            hide_index=True
        )

    # ========================================================
    # NULL PROFILE
    # ========================================================

    st.subheader("🔎 Null Value Profile")

    null_profile = pd.DataFrame({

        "Column": df.columns,

        "Null Count": [
            df[column].isna().sum()
            for column in df.columns
        ],

        "Null Percentage": [
            round(
                df[column].isna().mean() * 100,
                2
            )
            for column in df.columns
        ]

    })

    st.dataframe(
        null_profile,
        use_container_width=True,
        hide_index=True
    )

    # ========================================================
    # DUPLICATE PROFILE
    # ========================================================

    st.subheader("🔁 Duplicate Profile")

    if "customer_id" in df.columns:

        duplicate_count = (
            df["customer_id"]
            .duplicated()
            .sum()
        )

        unique_count = (
            df["customer_id"]
            .nunique()
        )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Duplicate Customer IDs",
                f"{duplicate_count:,}"
            )

        with col2:

            st.metric(
                "Unique Customer IDs",
                f"{unique_count:,}"
            )

    # ========================================================
    # DOWNLOAD CSV
    # ========================================================

    st.subheader("⬇️ Download Test Data")

    csv_data = df.to_csv(
        index=False
    ).encode("utf-8")

    file_name = (
        f"customer_test_data_"
        f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    )

    st.download_button(
        label="📥 Download Customer CSV",
        data=csv_data,
        file_name=file_name,
        mime="text/csv",
        use_container_width=True
    )

else:

    # ========================================================
    # INITIAL SCREEN
    # ========================================================

    st.info(
        "Configure the row count, columns and DQ scenarios "
        "from the sidebar and click "
        "**Generate Customer Data**."
    )

    st.markdown(
        """
        ### 🎯 Supported Data Quality Scenarios

        **Positive**
        - Valid customer records
        - Valid email
        - Valid phone
        - Valid business values

        **Duplicate**
        - Duplicate customer records
        - Useful for primary-key and duplicate checks

        **Null**
        - Random NULL values
        - Useful for mandatory-field validation

        **Invalid**
        - Invalid email
        - Invalid phone
        - Invalid status
        - Invalid numeric values
        - Invalid categorical values

        **Boundary**
        - Minimum/maximum credit score
        - Zero income
        - Empty strings
        - Boundary postal code
        - Boundary phone values
        """
    )

    st.markdown(
        """
        ### 🏗️ Typical ETL Testing Flow

        ```text
        Customer Test Data Generator
                    ↓
                CSV File
                    ↓
              Source System
                    ↓
               ETL Pipeline
                    ↓
             Bronze / Raw
                    ↓
               Silver
                    ↓
                 Gold
                    ↓
             DQ Validation
                    ↓
              PyTest Tests
                    ↓
             Test Execution
                    ↓
             Allure Report
        ```
        """
    )