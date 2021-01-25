# Specify parent image. Please select a fixed tag here.
ARG BASE_IMAGE=registry.git.rwth-aachen.de/jupyter/profiles/rwth-courses:2020-ss.1
FROM ${BASE_IMAGE}

# .. Or update conda base environment to match specifications in environment.yml
ADD environment.yml /tmp/environment.yml

# All packages specified in environment.yml are installed in the base environment
RUN conda env update -f /tmp/environment.yml && \
    conda clean -a -f -y
