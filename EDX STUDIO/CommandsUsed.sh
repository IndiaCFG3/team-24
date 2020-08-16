pip install tutor-openedx
tutor local quickstart
tutor local createuser --staff --superuser GunaSree gunasreesing@gmail.com

git clone https://github.com/overhangio/indigo
tutor config render --extra-config ./indigo/config.yml ./indigo/theme "$(tutor config printroot)/env/build/openedx/themes/indigo"
tutor images build openedx
tutor local start -d
tutor local settheme indigo localhost studio.localhost \$(tutor config printvalue LMS_HOST) $(tutor config p
tutor local quickstart


