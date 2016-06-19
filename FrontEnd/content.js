var app = angular.module('TabsApp', []);
app.controller('TabsCtrl', function($scope, $http) {
    $scope.url={base:'http://127.0.0.1:5000/address/api/v1.0/',people:'people/',companies:'companies/'};
    $scope.ids = {'intro': 'intro', 'companies': 'companies', 'people': 'people'};
    $scope.tabs = [ {
        id: $scope.ids.intro,
        title: 'Introduction'
    },{
        id: $scope.ids.companies,
            title: 'Organisations',
            url: 'organisations.tpl.html'
        }, {
        id: $scope.ids.people,
            title: 'People'
    }];

    $scope.currentId = $scope.ids.intro;
    $scope.onClickTab = function (tab) {
        if($scope.currentId === $scope.ids.companies){
            updateCompanies($scope.companies)
        }
        $scope.currentId = tab.id;
        if(tab.id === $scope.ids.companies){loadCompanies()}
        else if(tab.id === $scope.ids.people){loadPeople();loadCompanies();}
    };

    $scope.isActiveTab = function(tabId) {
        return tabId == $scope.currentId;
    };

    $scope.onToggle = function (item) {
        item.edit = !item.edit;
    };

    $scope.getName = function (person){
        var list = [];
        angular.forEach(['first_name','second_name'], function(item){
            if(person[item]){
                list.push(person[item])
            }
        });
        return list.join(" ");
    };

    $scope.getCompanyName = function(company_id) {
        var  len = $scope.companies.length;
        for (var i = 0; i < len; i++) {
            if (String($scope.companies[i].item_id) === company_id) {
                return $scope.companies[i].name;
            }
        }
        return null;
    };

    $scope.onSubmitCompany = function (myForm,companies) {
        if(myForm.$dirty) {
            updateCompanies(companies)
        }
        myForm.$setPristine();
    };

    var updateCompanies= function( companies){
        putCompanies(companies)
    };

    var putCompanies = function (data) {
        $http.put($scope.url.base + $scope.url.companies,data)
            .then(function (response) {
                loadCompanies();
            });
    };

    var loadCompanies = function () {
        $http.get($scope.url.base + $scope.url.companies)
            .then(function (response) {
                $scope.companies =response.data.companies;
                $scope.companies.push({edit:true});
            });
    };

    $scope.getAddress= function(company){
        var address = [];
        angular.forEach(['line1','line2','postcode','country'], function(item){
            if(company[item]!==undefined){
                address.push(company[item])
            }
        });
        return address.join("\n");

    };

    $scope.implode = function(object){
        var list=[];
        angular.forEach(object,function(value,key){list.push(value)});
        return list.join("\n");
    };
    

    var loadPeople = function () {
        $http.get($scope.url.base + $scope.url.people)
            .then(function (response) {
                $scope.people = response.data.people;
                $scope.people.push({edit:true});
            });
    };
    

});