var app = angular.module('TabsApp', []);
app.controller('TabsCtrl', function($scope, $http) {
    $scope.url={base:'http://127.0.0.1:5000/address/api/v1.0/',people:'people/',companies:'companies/'};
    $scope.ids = {'intro': 'intro', 'companies': 'companies', 'people': 'people'};
    $scope.tabs = [ {
        id: $scope.ids.intro,
        title: 'Introduction',
        url: 'introduction.tpl.html'
    },{
        id: $scope.ids.companies,
            title: 'Organisations',
            url: 'organisations.tpl.html'
        }, {
        id: $scope.ids.people,
            title: 'People',
            url: 'people.tpl.html'
    }];

    $scope.currentTab = 'introduction.tpl.html';

    $scope.people=[];
    $scope.organisations=[];

    $scope.onClickTab = function (tab) {
        $scope.currentTab = tab.url;
        if(tab.id === $scope.ids.companies){$scope.loadCompanies()}
    };

    $scope.onClickCompanyPlus = function (company) {
        debugger;
    };

    $scope.loadCompanies = function () {
        $http.get($scope.url.base + $scope.url.companies)
            .then(function (response) {
                $scope.companies = $scope.processCompanies(response.data.companies);
            });
    };

    $scope.processCompanies = function(rawCompanies){
        debugger;

        var companies = [];
        angular.forEach(rawCompanies, function(company){
            company.emailTxt = implode(company.emails);
            company.phoneTxt = implode(company.phones);
            company.addressTxt = getAddress(company);
            companies.push(company);
        });
        console.log(companies);
        return companies;
    };

    var getAddress= function(company){
        var address = [];
        angular.forEach(['line1','line2','postcode','country'], function(item){
            if(company[item]!==undefined){
                address.push(company[item])
            }
        });
        return address.join("\n");

    };

    var implode = function(object){
        var list=[];
        angular.forEach(object,function(value,key){list.push(value)});
        return list.join("\n");
    };

    $scope.loadPeople = function(){
        debugger;
        $http.get($scope.url.base+$scope.url.people)
            .then(function (response) {$scope.people = response.data.people;
            });
    };

    $scope.isActiveTab = function(tabUrl) {
        return tabUrl == $scope.currentTab;
    }
});