FROM python:3.8

ENV AZURE_TENANT_ID=dab167d2-fdab-4ab5-a387-22f955436d0a
ENV AZURE_CLIENT_ID=dcbed37e-c2a7-483f-85a9-2870a379684f
ENV AZURE_CLIENT_SECRET=o~68Q~zefCPPqejyKmGQC4FPNhhf143SkZtKtb-y

ENV PYTHONUNBUFFERED 1
ENV DockerHOME=ossDjango
ENV APPLICATIONINSIGHTS_CONNECTION_STRING=InstrumentationKey=6e1349bc-cb25-4fe2-a775-3d804e8d2c7c;IngestionEndpoint=https://australiaeast-1.in.applicationinsights.azure.com/;LiveEndpoint=https://australiaeast.livediagnostics.monitor.azure.com/

RUN mkdir -p $DockerHOME 

WORKDIR $DockerHOME

RUN pip install --upgrade pip 

COPY . $DockerHOME  

# RUN echo $(ls -1 /tmp/dir)
# RUN echo $(ls)

RUN cd $DockerHOME && pip install -r requirements.txt
# RUN echo $(ls)
# RUN ls && echo asds


# RUN pip install -r requirements.txt

EXPOSE 8000

CMD cd $DockerHOME && python manage.py runserver 0.0.0.0:8000