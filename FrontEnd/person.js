var app = angular.module('personApp', []);
app.controller('personCtrl', function($scope, $http) {
    $scope.confirm = function() {
        debugger;
        $scope.submitted = true;
    };

    $http.get("http://127.0.0.1:5000/address/api/v1.0/people/1")
        .then(function (response) {$scope.person = response.data.person;
            debugger;

        });
});