#Docker build for development environment.
FROM ruby:2.2.4

# Install necessary packages for building gem native extensions
# Nodejs is needed for installing uglifier
RUN apt-get update -qq && apt-get install -y build-essential libpq-dev
RUN curl -sL https://deb.nodesource.com/setup_6.x | bash -
RUN apt-get install -y nodejs

RUN mkdir /myapp
WORKDIR /myapp
ADD Gemfile /myapp/Gemfile
ADD Gemfile.lock /myapp/Gemfile.lock

# Nokogiri issue bandaid fix
RUN bundle config build.nokogiri --use-system-libraries
RUN bundle install
ADD . /myapp

RUN npm install
EXPOSE 3000

RUN bundle exec rake assets:precompile
CMD ["bundle", "exec", "rails", "server", "-b", "0.0.0.0"]
