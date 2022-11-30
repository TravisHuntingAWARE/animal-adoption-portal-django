#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from opentelemetry import trace
from opentelemetry.instrumentation.django import DjangoInstrumentor
from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace import TracerProvider

def main():
    """Run administrative tasks."""
    # WEBSITE_HOSTNAME is a special environment variable set by Azure,
    # you can read more here https://docs.microsoft.com/en-us/azure/app-service/configure-language-python#production-settings-for-django-apps
    settings_module = 'azuresite.production_settings' if 'WEBSITE_HOSTNAME' in os.environ else 'azuresite.development_settings'
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)


    tracer_provider = TracerProvider()
    trace.set_tracer_provider(tracer_provider)
    tracer = trace.get_tracer(__name__)
    
    django_instrumentor = DjangoInstrumentor()       
    django_instrumentor.instrument()

    azure_monitor_trace_exporter = AzureMonitorTraceExporter.from_connection_string(
        os.environ["APPLICATIONINSIGHTS_CONNECTION_STRING"]
    )

    # Batch the exports to AzureMonitor using a batch span processor. This will periodically
    # flush out "spans" to Azure Monitor in its own worker thread.
    batch_span_processor   = BatchSpanProcessor(azure_monitor_trace_exporter)

    tracer_provider.add_span_processor(batch_span_processor)

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
