FROM alpine

# Make user admin with home directory
RUN adduser -h /home/admin admin --disabled-password

WORKDIR /home/admin/Documents

RUN echo "172-17-0002" > social_security_number.txt
RUN echo "bcactf{imag3_PROc3sSINg_yaY_2ea104d700c1a8}" > not_social_security_number.txt

ENTRYPOINT ["tail", "-f", "/dev/null"]